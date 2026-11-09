"""Google Drive Uploader and Synchronization utility for research papers."""

from __future__ import annotations

import argparse
import logging
import mimetypes
import os
import sys
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger("gdrive_uploader")

DEFAULT_DRIVE_FOLDER_ID = "1J9aIr3WhsgWTKj3wCvGUUNSG8k9bLALk"
SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


class GoogleDriveUploader:
    """Uploads staged research papers and manifests to Google Drive."""

    def __init__(
        self,
        folder_id: str = DEFAULT_DRIVE_FOLDER_ID,
        credentials_file: Optional[str] = None,
        base_dir: Optional[str | Path] = None,
    ):
        self.folder_id = folder_id
        self.credentials_file = credentials_file or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent / "data"
        else:
            self.base_dir = Path(base_dir)

        self.papers_dir = self.base_dir / "papers"
        self.manifest_dir = self.base_dir / "manifests"
        self._service = None

    def authenticate(self) -> bool:
        """Authenticate with Google Drive API using available credentials."""
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build

            # 1. Check Service Account
            if self.credentials_file and Path(self.credentials_file).exists():
                creds = service_account.Credentials.from_service_account_file(
                    self.credentials_file, scopes=SCOPES
                )
                self._service = build("drive", "v3", credentials=creds)
                logger.info("Authenticated successfully via Service Account: %s", self.credentials_file)
                return True

            # 2. Check local client secret or token
            token_path = Path("token.json")
            cred_path = Path("credentials.json")

            creds = None
            if token_path.exists():
                from google.oauth2.credentials import Credentials
                creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                elif cred_path.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES)
                    creds = flow.run_local_server(port=0)
                    with open(token_path, "w") as token:
                        token.write(creds.to_json())

            if creds:
                self._service = build("drive", "v3", credentials=creds)
                logger.info("Authenticated successfully via Google OAuth.")
                return True

        except Exception as e:
            logger.warning("Google Drive authentication not yet configured: %s", e)

        return False

    def scan_staged_files(self) -> List[Path]:
        """Scan all staged papers, payload files, and manifests."""
        staged: List[Path] = []
        if self.manifest_dir.exists():
            staged.extend(self.manifest_dir.glob("*.jsonl"))

        db_path = self.base_dir / "papers.db"
        if db_path.exists():
            staged.append(db_path)

        if self.papers_dir.exists():
            for src_dir in [self.papers_dir / "arxiv", self.papers_dir / "openalex", self.papers_dir / "semanticscholar"]:
                if src_dir.exists():
                    staged.extend(src_dir.glob("*.json"))
                    staged.extend(src_dir.glob("*.pdf"))

        return staged

    def create_export_bundle(self, output_zip: Optional[Path] = None) -> Path:
        """Create a compressed zip package of all collected papers and manifests."""
        if output_zip is None:
            output_zip = self.base_dir / "research_papers_10000_bundle.zip"

        staged_files = self.scan_staged_files()
        logger.info("Creating export bundle with %d files into %s...", len(staged_files), output_zip)

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in staged_files:
                arcname = file_path.relative_to(self.base_dir)
                zf.write(file_path, arcname=str(arcname))

        logger.info("Export bundle created: %s (%.2f MB)", output_zip, output_zip.stat().st_size / (1024 * 1024))
        return output_zip

    def sync(self, dry_run: bool = False) -> Dict[str, Any]:
        """Upload staged files to the Google Drive folder."""
        staged_files = self.scan_staged_files()
        report: Dict[str, Any] = {
            "target_folder_id": self.folder_id,
            "total_staged_files": len(staged_files),
            "uploaded": 0,
            "skipped": 0,
            "dry_run": dry_run,
        }

        print(f"Target Google Drive Folder ID: {self.folder_id}")
        print(f"Staged files count: {len(staged_files):,}")

        if dry_run:
            print("[DRY-RUN] Files ready for upload:")
            for f in staged_files[:10]:
                print(f"  - {f.relative_to(self.base_dir)} ({f.stat().st_size:,} bytes)")
            if len(staged_files) > 10:
                print(f"  ... and {len(staged_files) - 10} more files.")
            return report

        if not self.authenticate():
            print("\n[NOTE] Google Drive API credentials (credentials.json or service_account.json) are not present.")
            print(f"Generating consolidated export zip bundle for direct upload to: https://drive.google.com/drive/folders/{self.folder_id}")
            bundle = self.create_export_bundle()
            report["export_bundle"] = str(bundle)
            print(f"Bundle successfully created at: {bundle}")
            return report

        # Upload files using Google Drive API
        from googleapiclient.http import MediaFileUpload

        for file_path in staged_files:
            try:
                mime_type, _ = mimetypes.guess_type(str(file_path))
                if not mime_type:
                    mime_type = "application/octet-stream"

                file_metadata = {
                    "name": file_path.name,
                    "parents": [self.folder_id],
                }
                media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
                uploaded = self._service.files().create(body=file_metadata, media_body=media, fields="id").execute()
                report["uploaded"] += 1
                logger.info("Uploaded %s -> Drive File ID: %s", file_path.name, uploaded.get("id"))
            except Exception as e:
                logger.error("Failed to upload %s: %s", file_path.name, e)
                report["skipped"] += 1

        return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Google Drive Sync for Collected Research Papers")
    parser.add_argument("--folder", type=str, default=DEFAULT_DRIVE_FOLDER_ID, help="Target Google Drive Folder ID")
    parser.add_argument("--credentials", type=str, default=None, help="Path to credentials.json or service_account.json")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run scan without uploading")
    parser.add_argument("--bundle-only", action="store_true", help="Generate zip bundle for manual upload")

    args = parser.parse_args()

    uploader = GoogleDriveUploader(folder_id=args.folder, credentials_file=args.credentials)

    if args.bundle_only:
        uploader.create_export_bundle()
        return

    uploader.sync(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
