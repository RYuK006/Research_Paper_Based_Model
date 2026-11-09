---
paper_id: "arxiv:chao-dyn/9810016"
title: "The color-flavor transformation and a new approach to quantum chaotic maps"
authors:
  - Martin R. Zirnbauer
year: 1998
doi: null
source: "arxiv"
parser_used: "arxiv_latex"
parsed_at: "2026-11-09T05:09:07.807238+00:00"
equation_count: 30
table_count: 0
---

# The color-flavor transformation and a new approach to quantum chaotic maps

## Abstract

The color-flavor transformation is a mathematical result that has applications to problems as diverse as lattice gauge theory, random network models, and dynamical systems. Several variants are described, and an outline of the proof is given. It is then shown how to use the transformation to set up a field theoretic formalism for quantum chaotic maps.

## Document Content

The Color-Flavor Transformation and a New Approach to
       Quantum Chaotic Maps}

  M R Zirnbauer
  
    Institut f\"{u}r Theoretische Physik, Universit\"{a}t zu K\"{o}ln,
    Germany.
    email: `zirn@thp.Uni-Koeln.de`.
  }
}

The color-flavor transformation is a mathematical result
  that has applications to problems as diverse as lattice gauge
  theory, random network models, and dynamical systems.  Several
  variants are described, and an outline of the proof is given.  It is
  then shown how to use the transformation to set up a field theoretic
  formalism for quantum chaotic maps.}

## Introduction

Building on the supersymmetric field theory of disordered conductors
and the lessons learned from it, Andreev et al. [a3s] have
recently proposed a fresh and, I think, exciting approach to quantum
Hamiltonian systems the classical dynamics of which is chaotic (see
the contribution of B.D. Simons to these proceedings).  To introduce
the subject of my talk, I wish to hint at another intriguing analogy,
which links quantum chaotic and disordered systems with the low energy
chiral sector of quantum chromodynamics (QCD).
Let me start by recalling that the low energy degrees of freedom of
QCD are particle-hole excitations, namely quark-antiquark states that
are called mesons (or pions).  The effective field theory governing
the mesons and the interactions between them is known to be a
nonlinear $$ model.  Similarly, the long wave length degrees of
freedom of a disordered conductor are particle-hole like excitations,
namely diffusion modes, whose interactions are described again by a
field theory of the nonlinear $$ model type.  This analogy at
the superficial or phenomenological level has a firm basis in the
modeling of the systems.  Indeed, in the strong coupling limit of
lattice QCD the nonabelian gauge field seen by the quarks is
represented by matrices placed on the links of the lattice and drawn
at random from the gauge group ${ SU}(N)$.  Similarly, in models of
two-dimensional electrons in a strong magnetic field, random unitary
matrices modeling the disorder potential are assigned to the links of
a directed network.
A mathematical physicist will then ask how the reduction from random
unitary matrices on links to a nonlinear $$ model is achieved.
The first point of this talk is to report the recent discovery of a
reduction scheme which is { nonperturbative} and circumvents the
traditional use of diagrammatic techniques to resum the leading terms
in a perturbation expansion.  The new approach is based on an identity
that transforms a certain class of integrals over the gauge group
${ U}(N)$ into integrals over the corresponding mesonic or
``flavor'' degrees of freedom.  Taking the terminology from QCD, I
call this identity the { color-flavor transformation}.
Because of the associated gain in efficiency, the color-flavor
transformation most naturally applies to cases such as QCD in the
large-$N$ limit, where the number of colors is big and the number of
flavors small.  However, the transformation promises nontrivial
applications also in other cases.  It offers, in particular, the
possibility of constructing a supersymmetric field theory of quantized
symplectic maps.  More precisely, it allows to express ${ U}(1)$
phase averaged products of the Green's functions of such a map as
integrals over nonlinear $$ model fields.  The latter
presentation appears particularly well suited for extracting the
universal behavior that is expected on the basis of the
Bohigas-Giannoni-Schmit conjecture [bgs], stating that the
spectral statistics of quantum chaotic systems in the universal limit
is Wigner-Dyson.

## Color-Flavor Transformation

I'll start with a simple equation that motivates and illustrates the
general form of the transformation.  If $_0, _1$ are complex
fermionic sources, the following statement is immediate:
        \[
        _0^{2 { d}a \,  ( _{1} e^{ia} _{0}
         + _{0} e^{-i{a}} _{1} )
        = 2 ( 1 + _{1}_{0}_{0}_{1} )
        =  _{ C} {{ d}z { d}{ z}
           (1+{ z}z)^3}  ( z _{1} _{1}
          - z _{0} _{0} ) \;.
        \]
The first equality sign does the integral over $a$ (the ``random gauge
field''), and the second organizes the quartic term into bilinears
$( _1 _0  _0 _1 = -_1_1 
_0_0)$, which are sent back to the exponent by integrating
over the complex numbers.
Why isn't $_0$ paired with $_1$, and $_0$ with $
_1$?  The answer is that in the form given, the scheme permits the
following remarkable generalization:
        \[
        _{{ U}(N)} dU \,
         ( _{1^i U^{ij} _{0^j
        + _{0^j  U^{ij} _{1^i )
        = _{{ C}^{n n}} d_N(Z,{ Z}) \,
         ( _{1^i Z_{^{i}} _{1^i
        -{_{0^j { Z}_{^{i}} _{0^j
        ) \;,
        \]
which deals with the case of $n$ ``flavors'' ($,=1,...,n$), and
$N$ ``colors'' ($i,j=1,...,N$) transforming according to the vector
representation of the gauge group ${ U}(N)$.  The integration
measure $dU$ on the left-hand side is the Haar measure of ${
  U}(N)$.  Summation over repeated indices is always assumed.  The
integral on the right-hand side is over all complex $n n$
matrices $Z$, with adjoint ${Z^_{ =  Z_{$,
and
        \[
        d_N(Z, Z) = { const} 
        { Det}(1+Z^ Z)^{-2n-N} _{,=1}^{n}
        { d}Z_{ { d}{ Z}_{ \;.
        \]
The geometric content behind this expression is that the matrix $Z$
parameterizes the compact symmetric space $M = { U}(2n)/{ U}(n)
 { U}(n)$, and the ${ U}(2n)$-invariant volume form on $M$
pulls back to the integration measure $d_0(Z, Z)$.
Note that the above formula is justifiably called the {
  color-flavor transformation}.  On the left-hand side the flavor
degrees of freedom are uncoupled, and color interacts through the
gauge group element $U  { U}(N)$.  On the right-hand side, the
roles have been reversed: now it is the color degrees of freedom that
enter multiplicatively, while flavor interacts by the ``mesonic
field'' $Z$.
The integral on the left-hand side is of the type encountered in
lattice gauge theory with dynamical fermions.  I claim that by using
the color-flavor transformation one can in fact verify that large-$N$
quantum chromodynamics in the strong coupling limit is equivalent to a
weakly coupled theory of mesons [witten].  Whether the scheme can
be adapted to deal with the weak coupling (or asymptotically free)
limit of QCD is under investigation.
The above formula is just one out of a large number of variants:
enumerate}
 A similar formula holds for { bosonic} sources $$ instead
  of the fermionic $$.  To get the bosonic version, one simply
  makes the formal replacements $N  -N$ and $ Z  - Z$,
  and restricts the domain of integration by requiring $1-Z^ Z
  > 0$.  [These steps imply that $M$ is replaced by its noncompact
  analog ${ U}(n,n)/{ U}(n) { U}(n)$.]  Convergence of
  all integrals now requires $N  2n$.
 In Ref.~[mrz_circular] a supersymmetric version with $n$
  bosonic (B) and $n$ fermionic (F) flavors was proved.  More
  generally, the color-flavor transformation exists also for $n_{
    B} = n_{ F}$ bosonic and fermionic flavors, as long as $N
   2(n_{ B}-n_{ F})$.
 The gauge group ${ U}(N)$ can be replaced by any one of the
  compact Lie groups ${ O}(N)$ or ${ Sp}(N)$.  For ${ Sp}(N)$
  a supersymmetric version of the transformation formula was given in
  Ref.~[mrz_circular], and the case ${ SO}(N)$ will be
  discussed below.
 One can also pass from groups to symmetric spaces, that is to
  say a color-flavor transformation exists for all random matrix
  models based on one of the large families of Riemannian symmetric
  spaces of the compact type.  As an example, consider the set of
  symmetric unitary matrices $S$, which is isomorphic to ${
    U}(N)/{ O}(N)$. The trick that works in this case is to use the
  canonical projection ${ U}(N)  { U}(N)/{ O}(N)$ by $U
   UU^{ T} =: S$, in conjunction with the Gaussian integral
        \[
         ( ^i S^{ij} ^j ) =
         ( - ^k ^k +
        ^i U^{ik}^k + ^k U^{jk}^j ) \;.
        \]
Since the invariant measures match under projection, this relates the
integral over $S$ to an integral over $U  { U}(N)$, with the
number of flavors doubled.
enumerate}

## Outline of Proof

I'll sketch the general strategy at the example of bosonic sources
$_^i$ in the fundamental representation of the gauge group
${ SO}(N)$.  In this case, the claim is
        \[
        _{{ SO}(N)} dO \,
         ( _^i O^{ij} _^j )
        = _D d_N(Z, Z) \,
        ( ^i_{ Z_{^{i}}
        ^i_{ + { c.c.} ) \;.
        \]
The mesonic integral here runs over the set $D$ of all complex {
  symmetric} $n  n$ matrices $Z$ with $1- ZZ > 0$, and the
integration measure is
        \[
        d_N(Z, Z) = { const} 
        { Det}(1- ZZ)^{N-n-1} _{
        { d}Z_{ { d}{ Z}_{ \;.
        \]
The domain $D$ is diffeomorphic to the noncompact symmetric space
${ Sp}(n,{ R}) /{ U}(n)$.
For the purpose of proving the present version of the color-flavor
transformation, it is convenient to quantize the classical sources:
$_^i b_^i$, $_^i   b_^i$, where
$b, b$ are operators that satisfy the canonical boson commutation
relations $[b_^i, b_^j] = ^{ij} _{$ and
act in a Fock space with vacuum $b_^i | 0  = 0$.  The set of
all single-boson operators $b b$, ${ b}{ b}$, and $ b b +
b b$ (indices omitted), define a representation of the symplectic
Lie algebra ${ sp}(nN,{ C})$ on Fock space.  Two prominent
subalgebras are ${ sp}(n,{ C})$ generated by the color
singlet operators ${b}_^{i} {b}_^{i}$, ${ b}_^{i} {
  b}_^{i}$ and ${ b}_^{i} b_^i + b_^i {
  b}_^{i}$, and ${ so}(N,{ C})$ generated by the flavor
singlet operators ${ b}_^i b_^j - { b}_^j b_^i$.
The latter subalgebra is the maximal subalgebra in ${
  sp}(nN,{ C})$ that commutes with the former, and vice versa.
Now we consider two types of coherent state:
        \[
        | =  ( _^{i} { b}_^{i} )
        | 0  \;,  { and} 
        | Z  =  ( { b}_^{i}
        Z_{^{i}} { b}_^{i} ) | 0  \;.
        \]
Their overlap is
        \[
          | {Z}  =  ( _^i
        Z_{^{i}} _^{i} ) \;.
        \]
By using standard results from Lie group theory, one shows that the
operator $P$ defined by
        \[
        P = _D d_N(Z, Z) \, | Z   Z |
        \]
projects Fock space onto the unique subspace that contains the vacuum
and carries an irreducible unitary group action $O  T_O := 
( { b}_^i ( O)^{ij} b_^j )$ of ${ SO}(N)$.
An alternative implementation of $P$ is by the Haar integral
        \[
        P = _{{ SO}(N)} dO \, T_O \;.
        \]
With these tools in hand, the color-flavor transformation is simply
proved by the following computation:
        

$$

        &&_D d_N(Z, Z) \, (_^i
        Z_{^{i}} _^i + { c.c.} )
        = _D d_N(Z, Z) \,   | Z 
         Z |    \\
        &&=   | P |  
        = _{{ SO}(N)} dO \
          | T_O |  
        = _{{ SO}(N)} dO \
         ( {_^i O^{ij} _^j ) \;.
        
$$

## Application to Quantum Maps

On a symplectic manifold $(M,)$ of dimension $2d$ consider a
symplectic map $ : M  M$.  Quantization will turn $$ into a
unitary operator $U$ on a Hilbert space ${ H}_N$ of finite
dimension $N = (2)^{-d} _{M}^{ d}$.  It is
then interesting to ask what one can say about the correlations
between the eigenvalues $e^{i_$ $(  \{1,...,N\})$ of
the quantum ``map'' $U$ when the classical map $$ is chaotic.
An informative statistic is the { pair correlation function} $C$.
Its value on a testfunction $f : { U}(1)  { R}$ is
defined to be
        \[
        C[f] = {2 N^2} _{,=1}^N
        f ( e^{i(_ - _)} ) -
        _0^{2 f(e^{i) { d} \;.
        \]
Given the Fourier expansion $f(e^{i) = (2)^{-1} _{l
  { Z}} { f}_l \; e^{il$, the pair correlation
function can be written in the equivalent form
        \[
        C[f] = {2 N^2} _{l=1}^ { Re}{ f}_l \;
        | { Tr} U^l |^2 \;.
        \]
In the physics literature one usually considers a related object, the
so-called two-level correlation function $R_2$, which is obtained by
evaluating $C$ on the $$-distribution $_r = (2)^{-1}
_{l Z}} e^{il(-r)}$ centered at $r = 2 s/N$:
        \[
        R_2(s) = C[_{2 s/N}] = {2 N^2} _{l=1}^
        (2 s l/N) \; | { Tr} U^l |^2 \;.
        \]
For chaotic systems, very little is known about $R_2(s)$ (and other
correlation functions) from a rigorous standpoint.  There exists,
however, a conjecture by Bohigas, Giannoni and Schmit [bgs],
stating that the correlation functions for $N  $ tend to a
universal limit given by random-matrix theory.  In particular, the
two-level correlation function of chaotic systems with broken
time-reversal symmetry is predicted to be
        \[
        R_2(s) = (s) - {^2  s  ^2 s^2} \;.
        \]
It is a challenging and longstanding problem in mathematical physics
to specify the precise conditions on the quantum map $U$ under which
this conjecture holds true.
How does the color-flavor transformation come in here?  To that end,
consider the generating function
        \[
        _U(_+,_+;_-,_-)
        = { Det}(1-_+U)\,{ Det}(1-_-U^)}
        {{ Det}(1-_+U)\,{ Det}(1-_-U^)} \,,
        \]
where $_, _$ are complex numbers, and take an average
over the unit circle ${ S}^1$ in ${ C}$:
        \[
        _U(...) =
        _0^{2{d 2\, _{(i)U}(...)\;.
        \]
This average over the spectral domain ${ S}^1  { U}(1)$
of the unitary operator $U$ corresponds to the energy averaging
employed in the work of Andreev et al. [a3s] on Hamiltonian
systems.  It is an easy computation to show that the two-level
correlation function can be extracted from $_U$ by
        \[
        R_2(s) = {1 2N^2} { Re} {^2  
        '} _U ( e^{i+2 is/N},
        e^{-i+2 is/N} ; e^{-i'}, e^{i'} )
        |_{ = ' = 0} \;.
        \]
The starting point for setting up a field theoretic formalism for
quantum maps is the following formula:
        \[
        _U(_+;_-) = 
         ( - _+ ( 1 - _+  U ) _+
        - _- ( 1 - _-  U^ ) _- ) \;,
        \]
which expresses $_U$ as a Gaussian integral over ``supervectors''
$_$.  Here $_ = { diag}(_,_)$ acts
in a ${ Z}_2$-graded space ${ C}^{1|1}$, and $_$
are elements of what Berezin calls the Grassmann envelope of ${
  C}^{1|1}  { H}_N$.
In the next step we do the phase average $_U  _U$,
by applying the color-flavor transformation with $n = 1$ ``colors''
and $N = { dim}{ H}_N$ ``flavors''.  (Note that we have
switched notation $N  n$ to emphasize the inequality $N
 n$ in the present application of the transformation formula.)
Then, on carrying out the Gaussian superintegral over $,$
we get
        

$$

        _U (_+ ; _- ) =
        _{D_N} D_N(Z, Z) \, { SDet}(1- ZZ)
        \, { SDet} ( 1 -  Z (_+  U) Z
        (_-  U^) )^{-1} \;,
        
        
$$

where ${ SDet}$ is the superdeterminant.  The integration variables
$Z, Z$ are complex supermatrices,
        \[
        Z = Z^{ BB} &Z^{ BF}
                     Z^{ FB} &Z^{ FF}
        = _{,=1}^N \, _{,={ B,F}}
        Z_{^{ \, E_{ E_{ \;,
        \]
and similar for $ Z$, with the domain of integration $D_N$
defined by $ Z^{ FF} = -{Z^{ FF}}^$, $ Z^{
  BB} = {Z^{ BB}}^$, and $1-{Z^{ BB}}^ Z^{ BB}
> 0$.  To describe the integration measure, let $G_N = {
  GL}(2N|2N)$ and $H_N = { GL}(N|N) GL}(N|N)$, and define
$_N$ to be the map that takes $Z, Z$ into the super coset
space $G_N/H_N$ by
        \[
        _N(Z, Z) = 1 &Z  Z &1 H_N \;.
        \]
Then $D_N(Z, Z)$ arises by pulling back via $_N$ the
$G_N$-invariant Berezin measure on $G_N/H_N$.  It turns out that this
Berezin measure is locally flat:
        \[
        D_N(Z, Z) = _{,=1}^N
        { d}Z_{^{ BB} 
        { d}{ Z}_{^{ BB} 
        { d}Z_{^{ FF} 
        { d}{ Z}_{^{ FF}
        {^4 
         Z_{^{ BF}  Z}_{^{ BF}
         Z_{^{ FB}  Z}_{^{ FB}}
        + ... \;.
        \]
(The dots indicate global anomalies.)  By differentiating the
supersymmetric integral for $_U$ we obtain a formula for the
two-level correlation function:
        

$$

       &&R_2(Nx/2)={{ Re} 2N^2}_{D_N}D_N(Z, Z)\,
        { SDet}(1- ZZ)\,{ SDet}^{-1}(1-e^{ix} ZZ_U)
         \\
        &&2.8cm}
         ({ Tr} Z_U  Z (e^{-ix} - Z_U Z)^{-1}
         { Tr}  ZZ_U (e^{-ix} -  Z Z_U)^{-1}
         \\
        &&3.0cm}+\;e^{ix}{ Tr}Z_U Z(1-e^{ix}Z_U Z)
        ^{-1}_3 ZZ_U (1-e^{ix} ZZ_U)^{-1}) \;,
        
        
$$

where $Z_U = (1 U)Z(1 U^)$ and $_3 = {
  diag}(+1,-1)  1_N$.
While the steps done so far are exact and in fact rigorous, the
formula for $R_2(s)$ looks preposterous at first sight.  We have taken
a simple looking expression and transformed it into a horribly
complicated integral over a large supermatrix $Z$.  What's the
purpose?  The answer is that our formula promises to be a good
starting point for further analysis, at least for { chaotic} maps,
by the following reasoning.

## Zero Mode Approximation (heuristic)

The goal is to make a statement about $_U$ or $R_2$ in the
semiclassical limit.  Drawing the inspiration from recent work of
Andreev et al. [a3s], one might hope that for $ 
N^{-1/d}  0$, the integral (Omega) approaches a field
integral that will lend itself to evaluation by the methods of quantum
field theory.  However, as it stands, there is not much ground for
optimism.  Because there exists nothing that inhibits short wave
length fluctuations of the candidate field, the integral (Omega)
is certain { not} to converge to any well-defined field theory.
[Indeed, one can show that the integrand has $_{n=0}^N
N n^2$ critical points, all of which contribute with
comparable weight to $R_2(s)$ for small $s$.  In the semiclassical
limit these critical points correspond to point-like instantons placed
on the periodic orbits of the map $$, and the would-be field
theory looks like a dense gas of topological excitations.]
To make sense of the limit $N  $, one has no choice but to
introduce a { regulator}.  The natural procedure is to inject a
probabilistic component and do an ensemble average.  Thus, we will
abandon the ambition to treat an individual quantum map $U$ and,
instead, will average over a family of operators close to $U$, say
        \[
        U_ = e^{i^k X_k /  U \;,
        \]
where $X_1, ..., X_r$ are Hermitian $N N$ matrices that arise
from quantizing a set of Hamiltonian vector fields $_1, ...,_r$,
and the parameters $^1,...,^r$ are identically distributed
independent Gaussian random variables with zero mean and variance
$$.
Substituting $U_$ for $U$ in the expression for $$ and
taking the expected value, we obtain
        

$$

        &&E ( _{U_(_+;_-) )
        =  D_N(Z, Z) \; (-S) \;,  \\
        &&S = -  E ( { SDet}(1- ZZ) \; { SDet}
        (1 -  Z(_+  U_)Z(_- 
        U_^))^{-1} ) \;. 
        
$$

The function $S$ has a critical point at $Z =  Z = 0$.  For
$_+ = _- = 1_2$ this point extends to a supermanifold
$G_1/H_1$ of saddle points generated from $Z =  Z = 0$ by the
$G_1$-action
        

$$

        &&Z  g Z = (AZ+B)(CZ+D)^{-1} \;,  \\
        && Z  g  Z =
        (C+D Z)(A+B Z)^{-1} \;, 
        
$$

where $A = a  1_N$, $B = b  1_N$, etc.  It is known
from [a3s] that one gets the desired random matrix answer for
chaotic maps if one approximates the integral over $G_N/H_N$ by an
integral over the saddle point manifold $G_1/H_1$.  Hence, the natural
strategy is to try and justify this step, which is called the ``zero
mode approximation''.
The Hessian of $S$ at $Z =  Z = 0$ (and, by $G_1$-symmetry,
everywhere else on the saddle point manifold) is given by the
following combination of superdeterminants:
        \[
        S^{(2)} = { STr}  Z Z - E ( { STr}
         Z U_ Z U_^ )
        \]
if $_+ = _- = 1_2$.  From this we see that the stability
of the saddle point manifold is determined by the spectrum of $1 -
E(U_  U_^)$.  Prior to ensemble averaging the
operator $1 - U_  U_^$ has a large number $N$ of
zero modes (one for each eigenvector of $U_$), and the
single-zero-mode approximation fails.  With ensemble averaging, the
situation is much improved.  One then expects $N-1$ zero modes to
become ``massive'' (leaving only a single massless mode), provided
that (i) the classical map $$ is mixing, (ii) the squares of the
Hamiltonian vector fields $_1^2 + ... + _r^2$ add up to produce
an elliptic operator, and (iii) the parameter $$ is taken to
vary with $$ as $^$ where $ < 1$.  [This
conjecture comes from looking at the classical limit $1 - (
 _i _i^2)  ^*$ of the operator $1 - E( U_
 U_^)$.  Moreover, from power counting one estimates
that, in order to achieve the desired mass gap, a positive value of
the exponent $$ suffices, which means that all members of the
ensemble converge to give the same classical dynamics in the limit
$ 0$.]
Assuming the zero mode approximation to be justified, one arrives at
an integral over a $2  2$ supermatrix $$:
        \[
        E(_{U_ (_+ ; _-)) 
        _{D_1} D_1(,) \,
        { SDet}^N(1-) \,
        { SDet}^{-N}(1-_+_-) \;.
        \]
This integral is independent of $U$ and is easy enough to be worked
out in closed form:
        \[
        _{N
        E(_{U_(e^{ia_+/N},e^{ib_+/N};
        e^{-ia_-/N},e^{-ib_-/N}))=
        1 - (a_+ - b_+)(a_- - b_-)}{(a_+ - a_-)
         (b_+ - b_-)} ( 1-e^{i(b_+ - b_-)} ) \;.
        \]
For the two-level correlation function one obtains $E(R_2(s)) = 
(s) - ^2( s)/( s)^2$, in agreement with the random-matrix
conjecture by Bohigas, Giannoni, and Schmit.
Clearly, there are many details that need to be filled in here.
Nonetheless, I believe the above approach to be promising and to have
the potential of leading to rigorous theorems.
{ Acknowledgment}. I would like to thank O. Agam and A. Altland for
discussions.  I especially thank S. Zelditch for making the suggestion
to compose the map $$ with a stochastic Hamiltonian flow.
thebibliography}{99}
a3s} A.V. Andreev, B.D. Simons, O. Agam, and B.L. Altshuler,
  Nucl. Phys. B { 482}, 536 (1996).
bgs} O. Bohigas, M.J. Giannoni, and C. Schmit, Phys. Rev.
  Lett. { 52}, 1 (1984).
witten} E. Witten, Nucl. Phys. B { 160}, 57 (1979).
mrz_circular} M.R. Zirnbauer, J. Phys. A { 29}, 7113 (1996).
thebibliography}
