---
paper_id: "arxiv:chao-dyn/9803022"
title: "Probing Physics of Magnetohydrodynamic Turbulence Using Direct Numerical Simulation"
authors:
  - Mahendra K. Verma
  - Gaurav Dar
year: 1998
doi: null
source: "arxiv"
parser_used: "arxiv_latex"
parsed_at: "2026-11-09T05:09:06.792659+00:00"
equation_count: 26
table_count: 0
---

# Probing Physics of Magnetohydrodynamic Turbulence Using Direct Numerical Simulation

## Abstract

The energy spectrum and the nolinear cascade rates of MHD turbulence is not clearly understood. We have addressed this problem using direct numerical simulation and analytical calculations. Our numerical simulations indicate that Kolmogorov-like phenomenology with $k^{-5/3}$ energy spectrum, rather than Kraichnan's $k^{-3/2}$, appears to be applicable in MHD turbulence. Here, we also construct a self-consistent renomalization group procedure in which the mean magnetic field gets renormalized, which in turns yields $k^{-5/3}$ energy spectrum. The numerical simulations also show that the fluid energy is transferred to magnetic energy. This result could shed light on the generation magnetic field as in dynamo mechanism.

## Document Content

Probing Physics of Magnetohydrodynamic Turbulence Using Direct Numerical
Simulation}
M.\ K.\ Verma and G. Dar \\
{ Department of Physics, Indian Institute of Technology,} \\ { Kanpur
208016, INDIA}}
 }

abstract}
The energy spectrum and the nolinear cascade rates of MHD turbulence is not
clearly understood. We have addressed this problem using direct numerical
simulation and analytical calculations. Our numerical simulations indicate
that Kolmogorov-like phenomenology with $k^{-5/3}$ energy spectrum, rather
than Kraichnan's $k^{-3/2}$, appears to be applicable in MHD turbulence.
Here, we also construct a self-consistent renomalization group procedure in
which the mean magnetic field gets renormalized, which in turns
yields $k^{-5/3}$
energy spectrum. The numerical simulations also show that the fluid energy
is transferred to magnetic energy. This result could shed light on the
generation magnetic field as in dynamo mechanism.
abstract}
\

## Introduction

The fluid parcels in a turbulent flow have random motion. However, the
random flow velocities obeys certain properties. Since most of the talks in
the conference dealt with chaos which also yields random signals, it is
important to contrast the difference between chaos and turbulence. Chaos can
occurs in a nonlinear system with a few (3-10) degrees of freedom, but a
turbulent system has many (order millions or more) degrees of freedom. Also,
a turbulent system may be chaotic; may not be chaotic such as in structures
(e.g., vortex street); or it may have both chaos and structure coexisting
with each other.
Turbulence is ubiquitous and is of very practical importance. Some of the
major applications are in mixing, aeroplane and high speed vehicle design,
atmospheric flows and weather prediction, astrophysical objects like stars,
jets, interplanetary medium etc. Even with its wide industrial, practical,
and theoretical importance, the understanding of turbulence is very weak.
There are many empirical laws from experiments and simulations. There are
some phenomenologies, the most famous among these is by Kolmogorov. There
only a few mathematically rigorous calculations, primarily Kraichnan's
direct interaction approximation, calculations based on renormalization
group etc. In this paper we will focus on some of the statistical properties
of velocity and magnetic fields in a turbulent magnetohydrodynamic (MHD)
plasma. We have attempted to review in a concise manner some of the
phenomenological, numerical, analytical work, and observations from the
solar wind, with an emphasis on our work (with D. A. Roberts, M. L.
Goldstein, J. K. Bhattacharjee, V. Eswaran).
Outline of the paper is as follows. Since the existing MHD turbulence
phenomenologies are motivated by Kolmogorov's fluid turbulence
phenomenology, we review Kolmogorov's arguments in section 2. In section 3
we review the existing MHD turbulence phenomenologies. Section 4 contains
the numerical results, which are compared with the predictions of the
turbulence phenomenologies. In section 5 we briefly report the cascade rates
of fluid and magnetic energies. Section 6 contains a renormalization group
scheme which provides a self-consistent procedure to obtain the effective
mean magnetic field. Section 7 contains conclusions.

## Fluid Turbulence

The fluid flows are described by Navier-Stokes equation, which is

$$

(   { t}+{ u}({ x,}t)
 ) { u}({ x,}t)=- 1  p(
{ x},t)+  ^2{ u}({ x,}t)

$$

where ${ u}({ x,}t)$ is the velocity field, $p({ x},t)$ is the
pressure field, $ $ is the density, and $ $ is the viscosity of the
fluid. We assume that the fluid is incompressible, which implies that $
  { u}({ x,}t)=0$. The above equation can be made
non-dimensional by scaling the variables by large length, velocity, and time
scales ($L,U,T$). The ratio of the nonlinear terms (II and III term) and the
viscous term (IV term) turns out to be $UL/ ,$ which is called the
Reynolds number. When the Reynolds number $Re$ is large (greater that 10,000
or so), we say that the flow is turbulent. Please note that unlike chaos,
there is no critical Reynolds number above which the flow becomes turbulent;
experiments exhibit transitions at different $Re$'s.
Analytic solution to the above equation is not known in turbulent regime.
The existence and uniqueness of the solution itself is not clear at this
moment. From the experiments it is known that the velocity field ${ u(x,}
t)$ is random. There is a range of scales present in the flow between the
energy feeding scale $(L)$ and the dissipation scale $( )$. This
intermediate range is called the inertial range. Kolmogorov conjectured that
the physics in this range does not depend on the energy feeding scale or the
dissipation scale; the energy distribution is homogeneous and isotropic; the
interaction between the velocity modes is local in the Fourier space; and
the energy cascade rate $ (k)$ is independent of $k$ under steady state.
Using these assumptions, the energy spectrum can be deduced immediately
using dimensional analysis. We find that one dimensional energy spectrum $
E(k)$ ($ E(k)dk=$ total energy) is given by

$$

E(k)=K_{Ko} ^{2/3}k^{-5/3}

$$

where $K_{Ko}$ is an universal constant called Kolmogorov's constant, $k$ is
the wavenumber. Note that the nonlinear energy cascade $ (k)$ is equal to
the dissipation rate and the energy supply rate of the fluid.
Experiments and simulations [exptsim] are in reasonable agreement with
the above phenomenology. There is a small deviation of the exponent from 5/3
which is attributed to intermittency phenomenon. The Kolmogorov
phenomenology described above is well supported by the calculations based on
Direct interaction approximations [Leslie], renormalization group
techniques [RG,Mac], self-consistent mode coupling etc.
Regarding dependence on dimensionality, a brief remark is in order here. In
two dimensions, there are two different powerlaw exponents, 5/3 for small
wavenumber and 3 for large wavenumber regimes. The origin of the exponent 3
is because of enstrophy conservation. We will not discuss this issue here.
After this brief introduction to fluid turbulence, now we turn to MHD
turbulence.

## MHD Turbulence

The incompressible MHD equations are

$$

array}{c}
(   { t}
{ B}_0  +{ z}^{ } 
) { z}^{ }=- 1  p_{tot}+ _{+}
^2{ z}^{ }+ _{-} ^2{ z}^{ } \\
  { z}^{ }=0
array}

$$

where ${ z^{ }=u b.}$ Here { u} is the velocity fluctuation,
{ b} is the magnetic field fluctuation in velocity units (scaled by $
(4  )^{-1/2}$) , ${ B_0}$ is the mean magnetic field in velocity
units, and $ _{ }=(   )/2,$where $ $ is the
resistivity. The field $p_{tot}$ is sum of thermal and magnetic pressure.
The Alfv\'en waves are the basic modes of incompressible MHD equations. In
absence of the nonlinear term $({ z}^{ }  ){ z}
^{ }$, ${ z}^{ }$ are the two independent modes travelling
antiparallel and parallel to the mean magnetic field. However, when the
nonlinear term is present, new modes are generated. These modes interact
with each other, which results in a turbulent behaviour of the fluctuations.
Magnetohydrodynamic (MHD) turbulence is more complex than the fluid
turbulence. There are several MHD turbulence phenomenologies. In the
following discussion we will state the arguments of Dobrowolny et al. 
{mhdkraich} from which we can obtain the existing MHD\ turbulence
phenomenologies. The nonlinear interactions modify the amplitudes of the
eddies. We assume that the interaction between the fluctuations are local in
wavenumber space, and that in one interaction, the eddies $z_k^{ }$
interact with the other eddies of similar sizes for time interval $
_k^{ }$. Then from Eq. (MHDz), the variation $ z_k^{ }$ in
the amplitudes of these eddies during these interval is given by

$$

 z_k^{ }  _k^{ }z_k^{+}z_k^{-}k.

$$

In $N$ such interactions, because of their stochastic nature, the amplitude
variation will be $ z_k^{ } N}( z_k^{ })$.
Therefore, the number of interactions $N^{ }$ it takes to obtain a
variation equal to its initial amplitude $z_k^{ }$ is

$$

N^{ }  1{k^2( z_k^{ }) ^2(  _k^{
}) ^2}

$$

and the corresponding time $T^{ }=N _k^{ }$ is

$$

T^{ }  1{k^2( z_k^{ }) ^2 _k^{ }}.

$$

The time scale of the energy transfer at wavenumber $k$ is assumed to be $
T^{ }$. Therefore, the fluxes $ ^{ }$ of the fluctuations $z_k^{
}$ can be estimated as

$$

 ^{ } ( z_k^{ }) ^2}{T^{ }} 
_k^{ }( z_k^{ }) ^2( z_k^{ }) ^2k^2.

$$

By choosing different interaction time-scales, one can obtain different
energy spectra. Kraichnan (1965) and Dobrowolny et al. (1980) 
{mhdkraich} argued that the interacting $z_k^{+}$ and $z_k^{-}$ modes will
get separated because of the mean magnetic field in one Alfv\'en time-scale.
Therefore, they chose Alfv\'en time scale $ _A=(kB_0)^{-1}$ as the
relevant time-scale and found that

$$

 ^{+}  ^{-} 
1{B_0}E^{+}(k)E^{-}(k)k^3= .

$$

If we assume that $E^{+}(k) E^{-}(k),$ then we immediately obtain

$$

E^{+}(k) E^{-}(k) ( B_0 ) ^{1/2}k^{-3/2}

$$

In absence of mean magnetic field, the magnetic field of the largest eddy
was taken as $B_0$. Kraichnan (1965) also argued that the fluid and magnetic
energies are equipartitioned. We refer the above phenomenology either as one
due to Dobrowolny et al. or the generalized Kraichnan's phenomenology.
If the nonlinear time-scale $ _{NL}^{ } (kz_k^{ })$ is
chosen as the interaction time-scales for the eddies $z_k^{ }$, we obtain

$$

 ^{ } ( z_k^{ }) ^2( z_k^{ }) k,

$$

which in turn leads to

$$

E^{ }(k)=K^{ }( ^{ })^{4/3}( ^{
})^{-2/3}k^{-5/3},

$$

where $K^{ }$ are constants, which we will refer to as Kolmogorov's
constants for MHD turbulence. Because of its similarity with Kolmogorov's
fluid turbulence phenomenology, we refer to this phenomenology as
Kolmogorov-like MHD turbulence phenomenology. This phenomenology was first
given by Marsch [Marsch]. It is also a limiting case of a more
generalized phenomenology constructed by Matthaeus and Zhou, Zhou and
Matthaeus [ZM], which is

$$

 ^{ }=A^2E^{+}(k)E^{-}(k)k^3}{B_0+kE^{ }(k)}}

$$

where $A$ is a constant. Here the small wavenumbers ($kE^{ }(k)}
B_0$) follow 5/3 spectrum, whereas the large wavenumbers ($kE^{ }(k)}
 B_0$) follow 3/2 spectrum.
After the discussion on these phenomenologies one would naturally ask which
of the phenomenologies is applicable in the solar wind. From the arguments
by Matthaeus and Zhou, and Zhou and Matthaeus [ZM] we see that
Kraichnan or Dobrowolny et al.'s phenomenology is expected to hold when $
B_0 kE^{ }(k)}$; on the other hand Kolmogorov-like phenomenology
is expected to be applicable when $B_0 kE^{ }(k)}$. We would
like to test these scaling arguments from the solar wind observations and
simulations. In the solar wind, which is a good test ground for MHD
turbulence theories, we find that the exponent of the total energy is $
1.69 0.08$, whereas the exponent of the magnetic energy is $1.73 0.08$
[MG82], somewhat closer to 5/3 than 3/2. This is more surprising
because $B_0 kE^{ }(k)}$ for inertial range wavenumbers in the
solar wind. Also, in the solar wind we do not find a break from 5/3 to 3/2
spectrum as predicted by Matthaeus and Zhou, Zhou and Matthaeus 
{ZM,Verma:sim}. Hence, from the comparison with the solar wind observations,
it appears that there is some inconsistency in the phenomenological
arguments given above. To explore these issues further, we performed
numerical simulations and some analytic studies. As we will described below,
the numerical simulations also tend to indicate that the Kolmogorov-like
phenomenology, rather than Kraichnan's or Dobrowolny et al.'s phenomenology,
is probably applicable in MHD turbulence.
We have applied renormalization groups to analyse the above equations. We
find that under certain assumptions, $B_0$ gets renormalized as we go from
large length-scales to smaller length-scales. In other words, $B_0$
appearing in the Kraichnan's or Dobrowolny et al.'s argument must be $k$
dependent. This leads to $k^{-5/3}\,$energy spectra, which appears to be
consistent with the solar wind observations and the simulation results. We
will describe these ideas in more detail in the following sections.
Before we proceed further, we point out that the normalized cross helicity $
 _c$, defined as $(E^{+}-E^{-})/(E^{+}+E^{-})$, and the Alfv\'en ratio
$r_A$, defined as the ratio of fluid energy and magnetic energy, play an
important role in MHD turbulence.

## Numerical Simulation

To probe numerically the physics at the inertial range, one usually solves
the MHD equations using the pseudospectral method with introduction of
hyperviscosity and hyperrestivity. For large resolution turbulence
simulations, spectral method is preferred over finite difference methods
because the derivatives can be calculated accurately using the Fourier
transforms. Note that any error in these equations could propagate very
fast, which could make the simulation unreliable. Most of our runs were
performed in two-dimensions because of the expense associated with large
three-dimensional runs. Fortunately, the scaling arguments described in the
earlier section does not depend on the dimensionality because the absolute
equilibrium theories predict a forward cascade of total energy in both two
and three dimensions. The simulation method is as follows.
The equations are time advance in Fourier space. The nonlinear terms are
calculated in real space, then its Fourier transform is calculated using
FFT. For details of the simulation, refer to Biskamp and Welter [MHDsim]
and Verma et al. [Verma:sim]. Earlier high resolution simulations were
performed by Biskamp and Welter (1989), Pouquet et al. (1988), and Politano
et al. (1989) [MHDsim]. In all these simulations there was no strong
evidence for either 3/2 or 5/3 spectral evidence.
We have taken $ = ,$ (or $ _{-}=0$) in our simulation. The
viscous term has been modified by an addition of hyperviscous and
hyperresistive term. The modified viscous term is

$$

 (  ^2+ ^4}{k_{eq}^2})
{ z}^{ }.

$$

Our $ =5.0 10^{-6}$, but $k_{eq}=10.0$ which yields Reynolds number
of approximately $2 10^5$ at large scales and 500 at small scales. The
maximum resolution of our simulation in 2D is $512^2$. The parameter $
dt=5.0 10^{-4}.$ The runs we consider have $( B_0,
_c) =(0,0),(0,0.25),(0,0.9),(1,0),(1,0.25),(1,0.9),(5,0.25),(5,0.9).$
The $ _c$ values are for $T=0$. We have taken the initial Alfv\'en
ratio to be 1.0. The simulation were initialized with a box spectrum out to $
k=4$ for $B_0=0$, and a $k^{-1}$ spectrum out to $k=15$ for $B_0=5.0$.
We find that after approximately $T=10$ the system has reached a fully
developed turbulent state, i.e., the energy spectrum shows approximate power
laws in the inertial range. We obtained the spectral indices by fitting a
straight line in the inertial range, and found that it was difficult to
distinguish between the indices 3/2 and 5/3. Therefore, we decided to study
the energy cascade rates $ ^{ }\,$ leaving a sphere of radius $K$ in
the wavenumber space which is given by

$$

 ^{ }(K)=-  { t}_0^KE^{ }(k,t)dk-2
_0^K[1+(k/k_{eq})]^2k^2E^{ }(k)dk.

$$

The cascade rates $ ^{ }(K)$ were calculated numerically and compared
with the predictions of the phenomenologies. The Kolmogorov-like
phenomenology predicts that $(E_k^{-}/E_k^{+})/( ^{-}/
^{+})^2=K^{-}/K^{+}$, while the Dobrowolny et al.'s phenomenology predicts
that $ ^{+}= ^{-}$. In our simulation we find that for initial $
_c=0$ and 0.25, $(E_k^{-}/E_k^{+})/( ^{-}/ ^{+})^2 1$. For
large $ _c$ this equality does not hold. Note that uncertainties is
quite large in our simulations. However, we found in all our runs that the
larger of $E_k^{+}$ and $E_k^{-}$ had larger cascade rate, thus negating
Dobrowolny et al.'s predictions. In our simulations the mean magnetic field
(or the magnetic field of the largest eddies) were at least $ 1$,
whereas the amplitudes of the largest $z^{ }$ fluctuations in the
inertial range $(k>10)$ were 0.2 to 0.5 (initial total energy = 1). Hence $
z^{ }<B_0$, and generalized Kraichnan's model should have been
applicable, but we find otherwise. Hence we conclude that our numerical
result are contrary to the predictions of the phenomenologies. The
Kolmogorov-like phenomenology appears to hold for small $ _c$ (with $
K^{+}=K^{-}$) in all $B_0=0-5$ regime. However, for large $ _c$, there
appears to be inconsistency. It is possible that the Kolmogorov-like
phenomenology may still hold for large $ _c$ with constants $K^{+}$
and $K^{-}$ being unequal and dependent on $ _c$. This issue is under
current investigation. (The details of the above simulation results are
described in Verma et al. [Verma:sim]).

## Cascade rates of magnetic and fluid energies

The origin of magnetic field in the earth, sun, and in the universe is an
important problem. It is generally believed that the fluid energy gets
transferred to the magnetic energy due to nonlinear interactions, a
mechanism know as dynamo. There are many models to get the desired magnetic
field configuration in the astrophysical objects. Here we have attempted to
investigate the cascade rates of magnetic and fluid energies. These studies
will shed light on the energy transfer mechanisms involved in dynamo
mechanism. Since this work is in progress, here we are reporting only the
preliminary results.
The equations for fluid and magnetic energies are as follows:

$$

(   { t}-2 k^2) u^2=-{
u  }p-{ u }[ { u  u
}] +{ u }[ { b  b}]

$$

$$

(   { t}-2 k^2) b^2={
b }[ { b  u}] -{ b }[
{ u  b}]

$$

The cascade rates by evaluating $-_0^KT(k)dk$ where $T(k)$'s are the
nonlinear terms appearing in the right hand side of the above equations. The
pressure term does not yield any energy transfer. The second term in the RHS
of Eq. (u2) yields the energy transfer from $u u$ $(
_{u})$, while the third term yields energy transfer $
u b(_{u b})$. The terms in the RHS\ of Eq. (
{b2}) primarily yield the energy transfer from $b u$ $(
^{total}_{b})$(the transfer from $b b$ has been ignored). The
total energy transfer rates coming from { u} and { b} spheres
of radius $K$ are $_{u}^{total}$ and $_{b}^{total}$ respectively.
We have obtained these cascade rates numerically.
We solve the MHD equations numerically one a $256 256$ grid using the
method described in the earlier section. We choose $ = =10^{-5}$, $
k_{eq}=10$, and initial $ _c=0,r_A=1.0$ . Note that there is no
forcing in our simulation. We have carried out our simulation till $T=7.5$.
On DEC 2000 4/233 the computer time required to reach $T=7.5$ was
approximately 4 hours. At $T=7.5$ we have calculated the cascade rates by
calculating the triple correlations. These cascade rates are shown in Figure
1. We find that $_{u b}$ is positive, while $
_{b}$ negative. At $k_{ }$ we have $_{u
b}=- _{b}^{total}$ Hence, there is a net transfer of energy from
the fluid energy to the magnetic energy. The energy evolution studies
indicate that the total fluid energy $(u^2/2)$ is decaying, while the
magnetic energy $(b^2/2)$ is almost constant in time. Hence, the dissipation
rate of magnetic energy appears to be balanced by the energy gained from the
transfer rate from the fluid energy. It is to be seen when the magnetic
energy get enhanced. In any case, these simulations show that there is a net
transfer of energy from velocity field to magnetic field. We also notice
that the energy cascade rate $_{u}$ is much smaller that
both $_{u b}$ and $_{b}^{total}$. Careful analysis
of the cascade rates for various parameter range is in progress.
We have attempted to obtain the perturbative solutions of MHD equations.
This is described below.

## Kolmogorov-like powerlaw using renormalization groups

There have been earlier attempts of applying renormalization groups 
{MHDrg} and other analytic technique, e.g.
Eddy-Damped-Quasi-Normal-Markovian approximation, to MHD\ turbulence. In
earlier renormalization group calculations, corrections to viscosity and
diffusivity are evaluated by the nonlinear terms in presence of forcing. In
our calculation presented here, we attempt to calculate corrections to the
mean magnetic field due to the nonlinear terms.
The basic idea of our calculation is to obtain the effective $B_0$ at higher
wavenumbers. In the phenomenology of Kraichnan and Dobrowolny et al. 
{mhdkraich} the external field or the magnetic field of the largest eddy is
taken to $B_0$. Here we construct a self-consistent scheme in which the
effective $B_0$ is taken to be the magnetic field of the next-largest eddy.
For example, for Alfv\'en waves of wavenumber $k$, the effective magnetic
field $B_0$ will be the magnetic field of the eddy of size $k/10$ or so.
This argument is based on the physical intuition that for the scattering of
the Alfv\'en waves at a wavenumber $k$, the effects of the magnetic field of
the next-largest eddy is much more than that of the external field. (For
similarity, please note that in WKB method , local inhomogeneity of the
medium determines the amplitude and phase evolution). We will find in the
following discussion that the $k$ dependent $B_0$ yields $k^{-5/3}$ energy
spectra. For simplicity we have taken $E^{+}(k)=E^{-}(k)$ and $r_A=1$.
The MHD equation in the Fourier space is [mhdkraich]

$$

 d{dt}z_i^{ }({ k},t) i( { B}_0
{ k}) z_i^{ }({ k},t)=
-i M_{ijm}({ k}) d{ p}z_j^{ }({ p},t)z_m^{ }({ k-p},t)

$$

where

$$

M_{ijm}({ k})=k_jP_{im}({ k});\ P_{im}({ k})= _{im}-
k_ik_m}{k^2},

$$

Here we have ignored the viscous terms. The above equation will, in
principle, yield an anisotropic energy spectra (different spectra along and
perpendicular to ${ B}_0$). Here we modify the above equation in the
following way to preserve isotropy

$$

 d{dt}z_i^{ }({ k},t) i( B_0k) z_i^{
}({ k},t)=-i M_{ijm}({ k}) d{ p}z_j^{ }({ p},t)z_m^{ }
({ k-p},t)

$$

This equation can be thought of as an effective equation with an isotropic
random mean field.
The calculation of $B_0(k)$ using the renormalization group is done by a
procedure adopted by McComb, McComb and Watt, Zhou et al., and others 
{Mac}. The wavenumber range $(k_0..K_N)$, is divided logarithmically into $N$
divisions. The $n$th shell is $(k_{n-1}..k_n)$ where $k_n=s^nk_o(s>1)$.
Brief summary of the RG operation used is given below (For details of the
procedure, refer to [Mac] and [Verma:rg]).
enumerate}
  Decompose the modes into the modes to be eliminated $(k^{<})$ and the
modes to be retained $(k^{>}).$ In the first iteration $(k_0..k_1)=k^{<}$
and $(k_1..k_N)=k^{>}$.
  We rewrite the Eq. (mhdk) for $k^{<}$ and $k^{>}$. The equation
for the retained modes are

$$

array}{c}
d}{dt}z_i^{ >}({ k},t) i( B_0(k)k)
z_i^{ >}({ k},t)=-i M_{ijm} ({ k})  d{ p}[
z_j^{ >}({ p},t)z_m^{ >}({ k-p},t)] + \\
[ z_j^{ >}({ p},t)z_m^{ <}({ k-p},t)
+z_j^{ <}({ p},t)z_m^{ >}({ k-p},t)+z_j^{ <}
({ p},t)z_m^{ <}({ k-p},t)]
array}

$$

We get a similar equation for $z_i^{ <}({ k},t)$ modes
  The terms given in the second bracket in the RHS of Eq. (MHDk)
is calculated perturbatively and the $z_i^{ <}({ k},t)$ modes are
averaged out. The effective equation after this operation is

$$

array}{c}
d}{dt}z_i^{ >}({ k},t) i
( [ B_0(k)+ B_0^{ }(k)] k)
z_i^{ >}({ k},t) \\
=-i M_{ijm}({ k}) d{ p}[
z_j^{ >}({ p},t)z_m^{ >}({ k-p},t)]
array}

$$

where

$$

 B_0^{ }(k)=- 12_{{ p+q=k}}d{ q}b_2(k,p,q)(
E(q)}{4 q^2}) (  1{pB_0(p)+qB_0(q)})

$$

The term $b_2(k,p,q)=kp(1+z^2)(z+xy),$where $x,y,z$ are the cosine of angles
between $({ p,q),(q,k),}$ and $({ k,p)}$ [Leslie]. Note that $
 B_0^{+}(k)= B_0^{-}(k)$ (for $E^{+}=E^{-}$ and $r_A=1$). Let us
denote

$$

B_1(k)=B_0(k)+ B_0(k)

$$

  We keep eliminating the shells by the above procedure. After $n+1$
iterations we obtain

$$

B_{n+1}(k)=B_n(k)+ B_n(k)

$$

where

$$

 B_n(k)=- 12_{{ p+q=k}}d{ q}b_2(k,p,q)(
E(q)}{4 q^2}) (  1{pB_n(p)+qB_n(q)})

$$

  We substitute the following forms for $E(k)$ and $B_n(k)$ in the Eqs.
(rg1,rg2) and solve for $B_n^{*}(k^{ })$ numerically 
{Mac,Verma:rg}.
$$
array}{c}
E(k)=  ^{2/3}k^{-5/3} \\
B_n(k_nk^{ })= ^{1/2} ^{1/3}k_n^{-1/3}B_n^{*}(k^{ })
array}
$$
We start with initial $B_0(k_i)$ at each shell, and keep iterating till $
B_{n+1}^{*}(k^{ }) B_n^{*}(k^{ })$, that is, till the
solution converges. We find that $B_n^{*}(k^{ })\ $is approximately
proportional to $k^{ -1/3}$. Hence, the mean magnetic field scales as $
k^{-1/3}$, and the energy spectra scales as $k^{-5/3}$ in this
self-consistent scheme.
enumerate}
Hence, we see that scaling of $B_0$ leads to $k^{-5/3}$ energy spectra. This
is a self-consistent scheme that shows the plausibility of Kolmogorov-like
energy spectra for MHD\ turbulence. Note that simulations and the solar wind
observations appear to favour the Kolmogorov-like phenomenology. Therefore,
the above analytical analysis is a promising step toward a proper
understanding of the statistical theory of MHD\ turbulence.

## Conclusions

In this paper we have reviewed some of the phenomenological, observational,
numerical, and analytic work in the statistical theory of MHD turbulence,
with emphasis on our studies. We find that the solar wind observations and
the numerical results are inconsistent with the predictions of the existing
MHD turbulence phenomenologies. The energy spectrum and the cascade rates
appear to be closer the predictions of Kolmogorov-like phenomenology even
when the mean magnetic field or the magnetic field of the largest eddies is
large compared to the inertial range velocity and magnetic field
fluctuations (a region where Kolmogorov-like theory is not expected to hold).
We have attempted to obtain Kolmogorov-like energy spectrum in MHD
turbulence in presence of arbitrary $B_0$ by postulating that the effective $
B_0$ is scale dependent, unlike what has been taken by Kraichnan and
Dobrowolny et al. We have constructed a renormalization group scheme and
shown that the self consistent $B_0(k) k^{-1/3}$ and $E(k)
k^{-5/3}$. This analysis has been worked out when $E^{+}=E^{-}$ and $r_A=1.$
The generalization to arbitrary parameters, or at least to the limiting
cases, is also planned. We will be able to the get the Kolmogorov's
constants for MHD\ turbulence analytically using this procedure; these
constants will be useful for the large-eddy-simulations (LES) of MHD
turbulence.
We have also carried out a preliminary study of the cascade rates of fluid
and magnetic energies. We find that there is a net transfer of fluid energy
to magnetic energy. We are investigating the parameter regimes in which
these cascade rates are large enough (more than dissipation rates) so that
the total magnetic energy increases with time, what is found in dynamo
theory.
Lastly, we would like to mention that the MHD turbulence theories are very
important for modelling various astrophysical phenomena and plasma
processes. We have estimated turbulent heating, nonclassical viscosity and
resistivity of the solar wind using the MHD turbulence phenomenologies 
{Verma:sw}. In this light, search for a satisfactory theory of MHD
turbulence appears quite important.
We thank all our collaborators, D. A. Roberts, M. L. Goldstein, J. K.
Bhattacharjee, and V. Eswaran. MKV\ also thanks V. Subrahmanyam, M. Barma,
V. Ravishankar, and D. Sa for numerous useful discussions.
thebibliography}{99}
exptsim}  H.\ L.\ Grant, R.\ W.\ Stewart, and A.\ Molliet, J.\
fluid Mech., { 12}, 241, 1962; U.~Frisch and P.\ Sulem, Phys.\ Fluids,
{ 27}, 1921, 1984.
RG}  V.\ Yakhot and S.\ A.\ Orszag, J.\ Sci.\ Comput., { 1}, 3,
1986; D.\ Ronis, Phys.\ Rev.\ A, { 36}, 3322, 1987; D.\ Forster, D.\
Nelson, and M.\ Stephen, Phys.\ Rev.\ A, { 16}, 732, 1977; For recent
calculations and reviews refer to articles in { Transition, Turbulence,
and Combustion}, ed. M. Y. Hussaini et al., Kluwer, 1994.
Mac}  W. D. McComb, Phys. Rev. A, { 26}, 1078, 1982; W. D.
McComb and V. Shanmugasundaram, Phys. Rev. A, { 28}, 2588, 1983; W. D.
McComb and A. G. Watt, Phys. Rev. A, { 46}, 4797, 1992; Y. Zhou, G.
Vahala, and M. Hussain, Phys. Rev. A, { 37}, 2590, 1988.
Leslie}  D.\ C.\ Leslie, { Developments in the theory of
Turbulence}, Claredon, Oxford, 1973.
mhdkraich}  R.\ H.\ Kraichnan, Phys.\ Fluids, { 8}, 1385, 1965;
M.\ Dobrowolny, A.\ Mangeney, and P.\ Veltri, Phys.\ Rev.\ Lett., { 45},
144, (1980).
ZM}  W.\ H.\ Matthaeus and Y.\ Zhou, Phys.\ Fluids, { B1}, 1929,
1989; Y.\ Zhou and W.\ H.\ Matthaeus, J.\ Geophys.\ Res., { 95}, 14881,
1990.
Marsch}  E.\ Marsch, in { Reviews of Modern Astronomy, Vol. 4},
ed. G.\ Klare, Springer-Verlog, 1990.
Verma:sim}  M. K. Verma, Ph. D. thesis, University of Maryland,
College Park, 1994; M.\ K.\ Verma, D.\ A.\ Roberts, M.\ L.\ Goldstein, S.\
Ghosh, and W.\ T.\ Stribling, J. Geophys. Res., { 101,} 21619, 1996.
MG82}  W.\ H.\ Matthaeus and M.\ L.\ Goldstein, J.~Geophys.~Res.,
{ 87}, 6011, 1982; E.\ Marsch and C.-Y. Tu, J.~Geophys.~Res., { 95},
8211, 1990.
MHDsim}  D. Biskamp and H. Welter, Phys. Fluids B, { 1}, 1964,
1989; H. Politano, A. Pouquet, and P. L. Sulem, Phys. Fluids B, { 1},
2330, 1989; A. Pouquet, P. L. Sulem, and M. Meneguzzi, Phys. Fluids, { 31}
, 2635, 1988.
MHDrg}  J.\ D.\ Fourrnier, P.\ L.\ Sulem, and A.\ Pouquet, J.\
Phys.\ A, { 15}, 1393, 1982; S.~J.~Camargo and H.\ Tasso, Phys.\ Fluids
B, { 4}(5), 1199, 1992.
Verma:rg}  M. K. Verma, preprint, to be submitted to Europhys.
Lett., 1998.
Verma:sw}  M.\ K.\ Verma, D. A. Roberts, and M. L. Goldstein, J.
Geophs. Res., { 100}, 19839, 1995; M.\ K.\ Verma, J. Geophys. Res., {
101}, 27543, 1996; { 101}, 27549, 1996.
thebibliography}
2.0cm}
center}
{ FIGURE CAPTIONS}
center}
0.5cm}
 Figure 1  This figure shows the fluxes for a simulation with initial
$_c=0.$ and $r_A=1.0$. The fluxes are found at $t=7.5$ when
$_c=0.015$ and $r_A=0.4$.
