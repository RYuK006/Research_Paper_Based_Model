---
paper_id: "arxiv:astro-ph/0211151"
title: "The superfluid two-stream instability and pulsar glitches"
authors:
  - N. Andersson
  - G. L. Comer
  - R. Prix
year: 2002
doi: null
source: "arxiv"
parser_used: "arxiv_latex"
parsed_at: "2026-11-09T05:09:02.771664+00:00"
equation_count: 79
table_count: 0
---

# The superfluid two-stream instability and pulsar glitches

## Abstract

This paper provides the first study of a new dynamical instability in superfluids. This instability is similar to the two-stream instability known to operate in plasmas. It is analogous to the Kelvin-Helmholtz instability, but has the distinguishing feature that the two fluids are interpenetrating. The instability sets in once the relative flow between the two components of the system reaches a critical level. Our analysis is based on the two-fluid equations that have been used to model the dynamics of the outer core of a neutron star, where superfluid neutrons are expected to coexist with superconducting protons and relativistic electrons. These equations are analogous to the standard Landau model for superfluid Helium. We study this instability for two different model problems. First we analyze a local dispersion relation for waves in a system where one fluid is at rest while the other flows at a constant rate. This provides a proof of principle of the existence of the two-stream instability for superfluids. Our second model problem concerns two rotating fluids confined within an infinitesimally thin spherical shell. The aim of this model is to assess whether the two-stream instability may be relevant (perhaps as a trigger mechanism) for pulsar glitches. Our results for this problem show that the entrainment effect could provide a sufficiently strong coupling for the instability to set in at a relative flow small enough to be astrophysically plausible.

## Document Content

n}}
p}}
e}}
b}}

{ A}}
{ B}}
{ C}}

_p}
{_}
{_}
{^2_}
{U_l^m}}
{V_l^m}}
{W_l^m}}
{V}_l^m}}
{W}_l^m}}
{U}_l^m}}
 v^r_
{ v^_}
{ v^_}
 v^r_
{ v^_}
{ v^_}
{ sin} 
{ cos} 
{ cot} 
{ tan} 
{   r}}
{   }
{   }
{E}}}
}

The superfluid two-stream instability and pulsar glitches}
[N. Andersson, G.L. Comer and R. Prix]
{N. Andersson$^$, G.L. Comer$^*$ and R. Prix$^$\\
$^$Department of Mathematics, University of Southampton, Southampton, SO17 1BJ, United
Kingdom \\$^*$Department of Physics, Saint
Louis University, St Louis, MO 63156,  USA}

abstract}
This paper provides the first study of a new dynamical instability in
superfluids. This instability is similar to the two-stream instability
known to operate in plasmas. It is analogous to the Kelvin-Helmholtz
instability, but has the distinguishing feature that
the two fluids are interpenetrating. The instability sets in once the relative
flow between the two components of the system reaches a critical level.
Our analysis is based on the two-fluid equations
that have been used to model the dynamics of the outer core
of a neutron star, where superfluid neutrons are expected to coexist
with superconducting protons and relativistic electrons. These equations
are analogous to the standard Landau model for superfluid Helium.
We study this instability for two different model problems.
First we analyze a local dispersion relation for waves in a system
where one fluid is at rest while the other flows at a constant rate.
This provides a proof of principle of the existence of the two-stream
instability for superfluids. Our second model problem concerns two rotating
fluids confined within an infinitesimally thin spherical shell.
The aim of this model is to assess whether
the two-stream instability may be relevant (perhaps as a trigger mechanism)
for pulsar glitches. Our results for this problem show
that the entrainment effect could provide a sufficiently strong coupling
for the instability
to set in at a relative flow small enough to be astrophysically
plausible.
abstract}

## Introduction

In this paper we describe a new dynamical instability
in superfluids.  This ``two-stream'' instability is analogous to the
Kelvin-Helmholtz instability drazin}.
Its key distinguishing feature is that the two fluids
are interpenetrating rather than in contact across an
interface as in the standard scenario.
The two-stream instability is well known in plasma
physics [where it is sometimes referred to as the ``Farley-Buneman''
instability
farley,buneman,buneman2}], and it has also been discussed in various
astrophysical
contexts like merging galaxies galax}
and pulsar magnetopheres pulsar1,pulsar2,pulsar3}, but as far as we
are aware it has not
been previously considered for superfluids.
In fact, the ``standard'' Kelvin-Helmholtz instability was only recently
discussed in the context of superfluids kh}.
The similarity of the equations used in plasma physics [a nice pedagogical
description of the plasma two-stream instability can be found in
[anderson]]
to the ones for two-fluid superfluid models inspired us to ask whether an
analogous instability could be relevant for
 superfluids. That this ought to be the case seemed inevitable.
To prove the veracity of this expectation, we
have adapted the arguments from the plasma problem to the superfluid case,
and discuss various aspects of the two-stream instability in this paper.
Of particular interest to us is the possibility that the two-stream
instability may operate in rotating superfluid neutron stars.
Mature neutron stars are expected to be
sufficiently cold (eg. below $10^9$~K) that their
interiors contain several superfluid/superconducting
components. Such loosely coupled components are usually invoked
to explain the enigmatic pulsar glitches, sudden spin-up
events where the observed spin rate jumps by as much as
one part in $10^6$ lyne}. Theoretical models for glitches
ruder,bppr,ai}
have been discussed ever since the first Vela pulsar glitch was observed
in 1969 vela1,vela2}, but these event are still not well understood.
After three decades of theoretical effort it is generally accepted that the
glitches arise because a superfluid component can rotate
at a rate different from that of the bulk  of the star, and that
a transfer of angular momentum from the superfluid to the crust
of the star could lead to the observed phenomenon.
The relaxation
following the glitch is well explained in terms
of vortex creep [see for example vcreep}], but the mechanism that
triggers the glitch event remains elusive. In this context, it seems
plausible that
the superfluid two-stream instability may turn out to be relevant.

## Proof of principle: A local analysis

### Superfluid dispersion relation

We take as our starting point the two-fluid
equations that  have been used to discuss the dynamics
of superfluid neutron stars mendell1,ac01,prix02}.
Hence, we consider superfluid neutrons (index $$) coexisting with
a conglomerate of charged components (index $$).
The constituents of the latter (mainly ions and electrons in
the neutron star crust and protons and electrons in the core)
are expected to be coupled by viscosity and the magnetic
field on a very short timescale. Hence, we assume that these charged
components will move together and that it is appropriate to treat them
as a single fluid.
The corresponding equations are ac01,prix02}

$$

_t n_X +  (n_X v}_X) = 0\,,

$$

where $n_X$ represent the respective number densities and $v}_X$ are the
two velocities. Here, and in the following, we use the constituent index $X$
which can be either $$ or $$. The respective mass densities are
obviously given by $_X = m_X\, n_X$} and we further introduce
the relative velocity $$ between the two fluids as

$$

  v}_ - v}_ \ .

$$

The first law of thermodynamics is defined by the differential of the
energy density or ``equation of state'',
$=(_, _, ^2)$}, namely

$$

  
  d = ^\, d_ + ^ \, d_ + \, d^2\,,

$$

which defines the chemical potentials $^X$ and the ``entrainment''
 function $$ as the thermodynamic conjugates to the densities and
the  relative velocity.
 With these definitions we can write the two Euler-type equations:

$$

  (_t + v}_) (v}_ + _  )
  +  ( + ^ ) + _
  _j  v_^j &=& 0\,,\\
  (_t + v}_) (v}_ - _  )
  +  ( + ^ ) - _
  _j  v_^j &=& 0\,,

$$

where we have introduced the dimensionless entrainment parameters

$$

_X  {2    _X}\,.

$$

The equation for the gravitational potential $$ is

$$

   ^2  = 4  G   \ , 

$$

where $ = _ +_$.
When $  0$ these equations make manifest the so-called entrainment effect.
The entrainment  arises
because the bare neutrons (or protons) are "dressed" by a polarization cloud of nucleons
comprised of both neutrons and protons.  Since both types of nucleon contribute to the
cloud the momentum of the neutrons, say, is modified so that it is a linear combination
of the neutron and proton particle number density currents (the same is true for the
proton momentum).  This means that when one of the fluids begins to flow it
will, through entrainment, induce a momentum in the other.
Because of entrainment a
portion of the protons (and electrons) will be pulled along with the superfluid neutrons
that surround the vortices by means of which the superfluid mimics
bulk rotation. This motion leads to magnetic fields being attached to the
vortices, and dissipative scattering of electrons off of
these magnetic fields. This ``mutual friction'' is expected to
provide one of the main dissipative mechanisms in superfluid neutron star cores mendell2}.
In order to establish the existence of the superfluid two-stream instability
we consider the following model problem: Let the unperturbed configuration be
such that the ``protons'' remain at rest, while the neutrons flow with
a constant velocity $v_0$. For simplicity, we neglect the
 coupling through entrainment ,
i.e. we take $ =0$,  and we also neglect perturbations in the
gravitational potential.
Under these assumptions, the two fluids are only coupled
``chemically'' through the equation of state.
Writing the two velocities as
$v}_ = [v_0+ v_(t,x)]x}$ and $v}_ = v_(t,x)x}$
where $ v_$ and $ v_$ are taken to be suitably small,
we get the perturbation equations

$$

_t  n_ + v_0 _x  n_ + n_ _x  v_ &=& 0 \ , \\
_t  n_  + n_ _x  v_ &=& 0 \ ,

$$

and

$$

_t  v_ + v_0 _x  v_ + _x   ^  &=& 0 \ , \\
_t  v_  + _x
 ^  &=& 0 \ .

$$

Next, we  assume harmonic dependence on both
$t$ and $x$, i.e. we use the Fourier decomposition
$ v_X(t,x) =  v_X  [i( t - kx)]$ etcetera.
This leads to the four equations

$$

i( - kv_0)  n_ - ik n_  v_ &=& 0 \ , \\
i  n_ - ik n_  v_ &=& 0 \ , \\
i( -kv_0)  v_ - ik  ^ &=& 0  \ , \\
i   v_ - ik  ^ &=& 0  \ .

$$

We thus have four equations relating the six unknown variables $ v_X$,
$ n_X$ and $ ^X$.
To close the system we need to provide an equation of state.
Given an energy functional ${ E} = { E} (n_,n_)$ we have

$$

m  ^ = . ( {     n_ }
) |_{n_  n_ +
. ( {     n_ }
) |_{n_  n_ =  { ^2 { E}    n_^2 }  n_ +  { ^2 { E}    n_  n_ }
 n_

$$

and similarly

$$

 m  ^ =  { ^2 { E}    n_  n_ }
 n_ +  { ^2 { E}    n_^2 }  n_ \ .

$$

Finally, we define the two sound speeds by, cf. ac01},

$$

c_^2  &=& n_ . {  ^   n_
|_{n_ = { n_  m} { { S}_{   { S}} \ , \\
c_^2  &=& n_ . {  ^   n_
|_{n_  = { n_ m} { { S}_{   { S}} \ ,

$$

and introduce the ``coupling parameter''

$$

{ C}  = n_ . {  ^   n_
|_{n_ = n_ . {  ^   n_
|_{n_= -  { n_  m} { { S}_{   { S}}\\

$$

which also has the dimension of a velocity squared.
For later convenience we have given the relation to the coefficients
of the ``structure matrix'' ${ S}_{XY}$ used by  prix}.
With these definitions we get

$$

n_  ^ &=&  c_^2   n_ + { C}  n_ \ , \\
n_   ^ &=& { n_  n_  { C}   n_ + c_{^2  n_ \ ,

$$

and we can rewrite our set of equations
as

$$

n_  v_ &=& ({   k} - v_0 )  n_ =
 ({   k} - v_0 )^{-1} [ c_^2   n_ + { C}  n_ ] \ , \\
n_  v_ &=& {   k}  n_ = { k  
[  { n_  n_  { C}   n_ + c_{^2  n_]
\ .

$$

Reshuffling we get

$$

[ ({   k} - v_0 )^2 - c_^2 ]  n_ &=&
 { C}  n_ \ , \\
[ ( {   k})^2 - c_^2 ] n_  &=&
  { n_  n_  { C}  n_ \ ,

$$

and a dispersion relation

$$

[ ({   k} - v_0 )^2 - c_^2 ][ ( {   k})^2 - c_^2 ] =  { n_  n_ { C}^2 \ .

$$

Introducing the ``pattern speed'' (the phase velocity)
$ = /k$ we have

$$

[ ( - v_0 )^2 - c_^2 ]
[ ^2 - c_^2 ] =  { n_  n_ { C}^2 \ .

$$

Not surprisingly,
this local dispersion relation is qualitatively similar to the one for the
plasma problem anderson}. We will now use it to investigate under what circumstances
we can have complex roots, i.e. a dynamical instability.

### The superfluid two-stream instability

First of all, it is easy to see that (disp0)  leads to
the simple roots

$$

 = \{ array}{ll}  c_ \\ v_0  c_ array}
.

$$

in the uncoupled case, when ${ C} = 0$.
This establishes the interpretation of $c_X$ as the sound speeds.
To investigate the coupled case, we introduce new variables
$x=/c_$ and $y=v_0/c_$. Then we get

$$

f(x,y) = { 1  a^2} [ (x-y)^2-1][x^2-b^2] = 1

$$

where we have defined

$$

a^2  { n_  n_ {{ C}^2  c_^4}
   and }  b^2  { c_{^2  c_^2} \ .

$$

The onset of dynamical
instability typically corresponds to the merger of two
real-frequency modes. If this is the case, a marginally stable configuration
will be such that  (fxy) has a double root. This happens when
an inflexion point of  $f(x,y)$ coincides with $f(x,y)=1$.
This is a useful criterion for searching for the marginally stable
modes of our system.
As a ``proof of principle'' we consider the particular case
of  $a^2=0.0249$ and $b^2=0.0379$ (we will motivate this particular choice
in Section~IIE).
The real and imaginary parts of the mode-frequencies for these
parameter values are shown as functions
of $y$ in Figure~modes. We have complex roots (an instability)
in the range $0.6 < y < 1.5$.
The corresponding mode frequencies lie in the range $0.03 < x_0< 0.36$. The
fastest growing instability occurs for $y  1.1$ for which
we find that $Im } x  0.17$. In other words, in this particular
case we encounter the two-stream instability once the  rate of the background flow is increased
beyond

$$

v_0 = c_ y  0.6 c_ \ .

$$

The corresponding frequency is given by

$$

 = k c_ x_0  0.1 k c_ \ .

$$

From this we see that the instability is
present  well before the neutron flow becomes ``supersonic''. This is crucial
since one would expect the superfluidity to be destroyed for
supersonic flows.
figure}

[height=6cm,clip]{PALfreq.eps}
Real (left panel) and imaginary (right panel) parts of the four roots of the
dispersion relation (fxy) for  model parameters
 $a^2=0.0249$ and $b^2=0.0379$. For these parameters the quartic dispersion relation
has four real roots for both
$y=0$ and $y=2$, while it has two real roots and a complex
conjugate pair for $y$ in the range $0.6<y<1.5$. In this range, the
two-stream instability is operating. The grey area corresponds to
$0  Re } x  1/2$ which is contained in the range of the
instability criteria discussed in Section~IIC. }

figure}
We have thus
established that the two-stream instability may, in principle, operate in
superfluids. Our example indicates the existence of a lower limit
of the background flow for the instability. This turns out to be
a generic feature.
In contrast, the plasma two-stream instability  can operate
at arbitrarily slow flows. An ideal plasma is unstable to
sufficiently long wavelengths for any given $v_0$.
In reality, however, one must also account for dissipative mechanisms.
In the case of real plasmas one finds that the so-called Landau
damping stabilizes
the longest wavelengths anderson}. Thus the two-stream instability
sets in below a critical wavelength in more realistic plasma models,
and there is typically (just like in the present case)
a range of flows for which the instability is present.
We will discuss the effects of dissipation on the superfluid two-stream
instability briefly in Section~IV.

### Necessary criteria for instability

It is useful to consider whether we can derive a necessary condition
for the two-stream instability.
To approach this problem in full generality would likely be quite
complicated, but we can  make good progress for the simple
one-dimensional toy problem discussed above.
We begin by multiplying the Euler equation (eul_n) for the neutrons by the complex conjugate
$ v^*_$. This leads to (after also using the continuity equations to replace
the perturbed number densities)

$$

(  -k v_0 - { k^2 c_^2   -kv_0} ) | v_|^2 =
{ C} {k^2 n_  n_   v^*_  v_ \ .

$$

Similarly, we obtain from the second Euler equation (eul_p)

$$

(   - { k^2 c_^2   ) | v_|^2 =
{ C} {k^2  - kv_0}  v^*_  v_ \ .

$$

Next we combine these two equations to get

$$

{ L} = { n_  n_  (  - v_0 - { c_^2  -v_0} )
|  v_|^2 + (-v_0) (  - { c_^2   ) |  v_|^2 =
{ C} (  v^*_  v_ +  v^*_  v_ )

$$

where we have introduced the pattern speed $$. From this expression we
see that the imaginary part of the left-hand side must vanish, so we should
have Im~${ L}=0$.
Allowing the pattern speed to be complex, i.e. using $ = _R + i _I$ we find that
the following condition must be satisfied

$$

Im } { L} = _R _I \{ { n_  n_
  [ 2 - { v_0  _R} (1- { c_^2 
  |-v_0|^2} )] |  v_|^2 + [ 2 - { v_0
   _R} ( 1 + { c_^2  ||^2} )]
|  v_|^2  \} = 0 \ .

$$

If we are to have an unstable mode, $_I 0$, the frequency clearly
must be such that  the factors multiplying the absolute values of the two velocities
have different signs.
Let us first consider the case when the
factor multiplying $| v_|^2$ is negative. Then we find that an instability is
only possible if ${_R/ v_0} <0$, and the following
condition is satisfied:

$$

0 < | {_R  v_0} | < {1  2} (
{ c_^2  | -v_0|^2} - 1 ) \ .

$$

This shows that we must have

$$

{ c_  |v_0|} > | {   v_0} -1 | >
| {_R  v_0} - 1 | = | {_R  v_0} | + 1 > 1

$$

which constrains the permissible frequencies to the range $|_R|< c_-|v_0|$.
Thus we see that the flow must be subsonic, i.e. $|v_0|<c_$.
In the case when the
factor multiplying $| v_|^2$ is negative we can
only have an instability if ${_R/ v_0} >0$.  We also require

$$

0 <  {_R v_0} < {1  2}  ( 1 + { c_^2  ||^2} ) <
{1  2}  ( 1 + { c_^2  _R^2} )
  if } 
|-v_0|^2 < c_^2

$$

or

$$

{ 1  2} ( 1 - { c_^2  |_R -v_0|^2})
<
{ 1  2} ( 1 - { c_^2  | -v_0|^2}) <
{_R v_0}
< {1  2}  ( 1 + { c_^2  _R^2} )
  if } 
|-v_0|^2 > c_^2 \ .

$$

For the example illustrated in Figure~modes, the condition that must be
satisfied is (cond1). It is useful to notice two things about this criterion.
First of all, any unstable mode for which $_R>c_$ must lie in the range
$0<c_<_R<v_0$. Secondly, when $_R>>c_$ the permissible
range will be well approximated by $0<_R<v_0/2$, cf. Figure~crit.
As is clear from Figure~modes the unstable modes satisfy this last, and most severe,
criterion.
figure}

[height=6cm,clip]{criteria.eps}
An illustration of the instability criterion (cond1)
which is relevant for the example considered in Section~IIB.
This example is constructed by introducing $z=_R/v_0$, and then showing
the four curves: $a(z)=z$, $b(z)=(1+^2/z^2)/2$, $c(z)= 1$ and
$d(z)=(z-1)^2$.
Here we have taken $c_^2/v_0^2=1$ and $^2= c_^2/c_^2=0.0379$.
Criterion (cond1) is satisfied when $d<c$ and $a<b$ (in the grey area).
The corresponding range is well approximated by  $0<_R/v_0<1/2$.  }

figure}
It is worth noting that the instability can be discussed in terms
of a simple energy argument [see casti} and pierce} for similar discussions in
other contexts].
After averaging over several wavelengths, the kinetic energy of the protons
is

$$

E_  {m_ n_  v_^2  2} > 0 \ .

$$

Meanwhile we get for the neutrons

$$

E_  { m_  2} (n_+ n_)(v_0+ v_)^2

$$

which leads to

$$

E_ 
{m_ n_  2}[ v_0^2 + { +kv_0  -kv_0}  v_^2 ]

$$

from which we see that the energy in the perturbed flow is smaller than the
energy in the unperturbed case, which means that we can associate the wave
with a ``negative energy'', when

$$

-v_0 < {   k} < v_0\ ,  i.e. }  -v_0 < _R <
v_0 \ .

$$

A wave that satisfies $0<_R<v_0$ moves forwards with respect to the protons
but backwards according to an observer riding along with the
unperturbed neutron flow. As we have seen above, the unstable modes in our problem
satisfy this criterion and hence it is easy
to explain the physical
conditions required for the two-stream instability to be present.

### Results for a simple model equation of state

Having established that the two-stream instability may be present in
superfluids, we want to assess to what extent one should expect this
mechanism to play a role for astrophysical neutron stars.
To do this we will consider two particular equations of state.
The results we obtain illustrate different facets of what we expect to
be a rich problem.
We begin by making contact with our recent analysis of rotating superfluid models
 prix} as well as the study of oscillating
non-rotating stars by pr02}.
From the definitions above we have

$$

a^2 &=& { n_  n_ { { S}_{^2  S}_{^2} \ , \\
b^2 &=&  { n_  n_ { { S}_{  S}_{} \ .

$$

We combine these results with the explicit structure matrix
given in eq. (144) of prix}, which is based on a simple
``analytic'' equation of state. This leads to

$$

a^2 &=&   { n_  n_ ^2 \ , \\
b^2 &=& 1 + {  (1-2x_)  1-x_ \ ,

$$

where $x_=n_/(n_+n_)$ is the proton fraction, and
 $$ is defined by

$$

 = { { S}_{  { S}_{ } \ .

$$

As discussed by prix},
$$ is related to the ``symmetry energy'' of the
equation of state, cf. PAL88}.
figure}

[height=6cm,clip]{newdomain.eps}
An illustration of the various domains of instability
for the simple ``analytic'' equation of state of prix}.
An absolute instability (see discussion in the main text) is active
in the grey areas (also labeled I and II). The two-stream instability
is, in principle, relevant in the remaining parameter space.
The dashed curves indicate the onset of instability
when the relative flow is equal to the neutron sound speed $(y=1$).
For slower flows, these critical curves approach the absolute instability
regions. The region where the two-stream instability may operate in
physical flows therefore lies between each dashed curve and the nearest grey area.
For comparison we also indicate the curve in the $x_-$ plane traced out by the PAL
equation of state (discussed in Section~IIE)
as the density is varied from that near the crust/core interface
($u=0.64$) to five times that of nuclear saturation $(u=5)$.}

figure}
The instability regions for this model equation of state
are illustrated in Figure~domain. A key feature of this
figure is the presence of regions of
 ``absolute instability''. This happens when $a^2>b^2$. Then
there exist unstable solutions already for vanishing background
flow, $y=0$.
That this is the case is easy to see. Consider $(fxy)$ in the limit
$y=0$. In the limit we can solve directly for $x^2$:

$$

x^2 = { 1 +b^2  2}   ( { 1 + b^2  2} )^2 - b^2 + a^2  }

$$

from which it is easy to see that one of the roots for  $x^2$
will be negative if $a^2>b^2$. Hence, one of the roots to the quartic
(fxy) will be purely imaginary.
The physics of this instability is quite different from the
two-stream instability that is the main focus of this paper.
Yet it is an interesting phenomenon. From the above relations
we find that  $a^2 < b^2$ corresponds to

$$

{ S}_{{ S}_{ > { S}_{^2 \ .

$$

In the discussion by prix} it was assumed that ``reasonable'' equations
of state ought to satisfy this condition. We expected this to be the case
since the structure matrix
would not be invertible if its
determinant were to vanish at some point. We now see that
this constraint has a strong physical motivation: The condition is
violated when $a^2>b^2$, i.e. when we have an absolute instability.
The regions where this instability is active are indicated by the grey areas
in Figure~domain.

### Results for the PAL equation of state

In order to strengthen the argument that the two-stream instability
may operate in astrophysical neutron stars, we have considered a
``realistic'' equation of state due to  Prakash, Ainsworth and
Lattimer (PAL) (1988). The advantage of this model is
that it is relatively simple. In particular, it leads to
analytical expressions for the various quantities
needed in our analysis. The energy density of the baryons for the PAL
equation of state can be written

$$

    { E}(n_,n_) = (n_ + n_) [E_0(u) + S(u) (1 -
                      2 x_)^2] \ ,

$$

where $E_0$ corresponds to the energy per nucleon, $S$
corresponds  to the ``symmetry energy'' (and is closely related to  $$ in the
``analytic'' equation of state discussed above), and $u = (n_ + n_)/n_0$ with  $n_0 = 0.16
\ { fm}^{-3}$ the nuclear saturation density.
$E_0$ takes the following form:

$$

    E_0(u) = A_0 u^{2/3} + B_0 u + C_0 u^ + 3 _{i = 1}^2 C_i
                _i^{-3} [_i u^{1/3} - 
                (_i u^{1/3})] \ ,

$$

with $A_0 = 22.11$ MeV, $B_0 = 220.47$ MeV, $C_0 = - 213.41$ MeV, $
= 0.927$, $C_1 = - 83.84$ MeV, $C_2 = 23.0$ MeV, $_1 = 2/3$, and
$_2=1/3$.  The symmetry term is

$$

    S(u) = A_S [u^{2/3} - F(u)] + S_0 F(u) \ ,

$$

with $A_S = 12.99$ MeV and $S_0 = 30$ MeV. Here $F(u)$ is a
function satisfying $F(1) = 1$ which is supposed to simulate the behaviour
of the potentials used in theoretical calculations.  In our study
we have only considered $F(u)=u$, which is one of four possibilities
discussed by PAL88}.
We further need to account for the energy contribution of the
electrons, which is important since the electrons are
highly relativistic inside neutron stars. Hence,  they can obtain
 high (local) Fermi energies which may be comparable with the proton (local)
Fermi energies.  Considering only the electrons, the leptonic
contribution to the energy density is given by (in units where the speed
of light is unity) shapiro}

$$

    { E}_{ = {m_  _^3}
                      (^{F}_) \ ,

$$

where $m_ = m_/1836$ is the electron mass (in terms of the baryon mass
$m_$), $_ = /m_$ is the electron Compton wavelength, and

$$

    (x) = {1  8 ^2} (x [1 + x^2]^{1/2}
              [1 + 2 x^2] - { ln}[x + (1 + x^2
              )^{1/2}]) \ ,

$$

$$

    ^{F}_ = 1836 (3 ^2 [{  m_b}]^3
                   )^{1/3} n_^{1/3} \ .

$$

In doing this calculation  we have assumed local
charge neutrality, i.e.  $n_=n_$.
The above energy term is added linearly in the equation of state.
Having obtained an expression for the total energy as a function of the
density, we can derive explicit expressions for all quantities needed to
discuss the two-stream instability. First we need to determine the proton fraction $x_$. We
do this by assuming that the star is in chemical equilibrium, i.e.

$$

^ = ^ + ^\,.

$$

Solving (chemeq) for $x_$ provides us with the proton fraction as
a function of $u$. Given this, and the relevant partial
derivatives of ${ E+E}_$ we can readily evaluate the symmetry energy
and well as the sound speeds $c_^2$, $c_^2$ and the chemical
coupling parameter ${ C}$.
With this data we can determine the two parameters $a^2$ and $b^2$
which are needed if we want to solve the local dispersion relation (fxy).
The results we obtain for the proton fraction and the symmetry energy are
indicated in Figure~domain. We consider the range from $u=0.64$, presumed to
correspond to the core-crust boundary, to $u=5$
which represents the deep core of a realistic neutron star.
The corresponding results for the two-stream instability are shown in Figure~local.
From this figure we can see that the two-stream instability may operate
(albeit at comparatively large relative flows) in the region immediately below
the crust. Finally,  we find that the conditions at the core-crust interface are such
that $a^2=0.0249$ and $b^2=0.0379$. These are  the values we chose for the
example in Section~IIB and hence the results shown in Figure~modes
correspond to a physically realistic model.
figure}

[height=6cm,clip]{localrange.eps}
Two-stream instability results for the PAL equation of state.
Left panel: The region where the two-stream instability is present (grey area)
is shown as a function of the density parameter $u$. We indicate the location of the
core-crust boundary ($u 0.64$) by a vertical dashed line. Our model is only relevant
for the core fluid, i.e. to the right of the vertical line. Finally, the horizontal dashed line indicates
when the relative flow is equal to the (neutron) sound speed. We expect the superfluid
degeneracy to be broken beyond this level, so an instability located above this
line is unlikely to have physical relevance. The results indicate that there
may be a region of instability immediately below the crust. Right panel: The corresponding
oscillation frequencies. Particularly notable is the point near $u=2$ where the
two critical curves cross. At this point the symmetry energy $$ changes sign, cf.
Fig.~domain, and there
exist a particular density such that the two fluids are uncoupled, cf. (adef).  }

figure}

## Rotating shells: A connection with pulsar glitches?

The fact that a superfluid neutron star may, in principle, exhibit the
two-stream instability does not necessarily prove that this
mechanism will be astrophysically relevant.
Yet, it is an intriguing possibility given that
the mechanism underlying the enigmatic glitches observed in dozens of
pulsars remains poorly understood. One plausible astrophysical
role for the superfluid two-stream instability would be in this
context: Perhaps this instability serves as trigger
mechanism for large pulsar glitches?

### Dispersion relation for rotating shells

Our aim in this Section is to construct a toy problem that allows
us to investigate a possible connection between the
two-stream instability and pulsar glitches.
A suitably simple problem corresponds to two fluids,  allowed to rotate at different
rates, confined within an infinitesimally thin spherical shell.
By assuming that the shell is infinitesimal we ignore radial motion, i.e. we restrict
the permissible perturbations of this system is such a way that
the perturbed velocities must take the form

$$

     v}_X
=  - {1  R    U^X_{lm}(t)
                          _ Y^m_l e}_
+ {1  R }  U^X_{lm}(t)
                        _ Y^m_l  e}_

$$

where  $Y^m_l(,)$ are the spherical harmonics and $R$ is the radius $R$
of the shell. This means that the system permits only
toroidal mode-solutions. In other words, all oscillation modes
of this shell model are closely related to the inertial r-modes
of rotating single fluid objects pandp,provost}.
The perturbation equations for the configuration we consider
have been derived in a different context and the complete
calculation will be presented elsewhere inert2}. Our primary interest
here concerns whether the modes of this system
may suffer the two-stream instability.
The presence of the instability in this
toy problem would be a strong indication that it will also be
relevant when the shells are ``thick''
and radial motion is possible.
That is, when we consider a rotating star
that contains a partially decoupled superfluid either
in the inner crust or the core.
As discussed in Section~IIC, the two-stream instability
can be understood in terms of negative energy waves.
In the current problem, the criterion for waves to carry
negative energy according to one fluid but positive
energy according to the other fluid is that the mode pattern
speed [we are assuming a decomposition $(i t + im)$]

$$

 = - {   m}

$$

lies between the two (uniform) rotation rates.
In other words, a necessary condition for instability is

$$

_ <  < _

$$

where we have assumed that the superfluid neutrons lag behind the
charged component, as is expected in a spinning down pulsar.
After a somewhat laborious calculation,
see inert2} for
details,  one finds that
the dispersion relation for the toroidal two-fluid modes of the
shell problem is

$$

    && \{ - l (l + 1) (1 - _
          ) [ + m _] + 2 m _ + m
          _ [2 - l (l + 1)]
          [_ - _]\}
       &&  \{ - l (l + 1) (1 - _ )
[ + m _] + 2 m
          _ + m _ [2 - l (l +
          1)][_ - _]\} 
       && - \{ l (l + 1))^2 _ _
( + m _) ( + m
          _\} = 0 \ .

$$

This equation should be valid under the conditions in
the outer core of a mature
neutron star, where superfluid neutrons are
permeated by superconducting protons.
We rewrite this dispersion relation in terms of the entrainment
parameter used by prix}, namely

$$

 = _ = { 2   _ \ ,

$$

the frequency as measured with respect to the rotation of the protons,

$$

 = {   m_ \ ,

$$

and a dimensionless measure of the relative rotation,

$$

={ _  _ \ .

$$

With these definitions we get

$$

&& \{ l(l+1) [1-x_(1+)](+) -2(1-x_) + x_ (l-1)(l+2)
(1-) \} \\
&& 
 \{ l(l+1) [1-](+1) -2 -  (l-1)(l+2)
(1-) \}  \\
&& - [l(l+1)]^2 x_ ^2 (+)(+1) = 0 \ .

$$

In terms of these new variables a mode would satisfy the necessary
instability criterion (nec_crit) if $$ is such that

$$

- << -1 \ .

$$

As we will now establish, there exist modes that satisfy this
criterion for reasonable parameter values.

### An extreme example: The quadrupole modes

Let us first consider the case of quadrupole oscillations, i.e. take $l=2$.
Typical results for this case are shown in Figures~shell and  rotfreq.
The first figure illustrates the regions of the $x_-$ parameter
space for which an instability is present in the case when (i)
the neutrons rotate at a rate that is 90\% faster than that of the
charged component, and (ii) the neutrons lag behind by the same fraction.
The second figure shows the  mode-frequencies
corresponding to the second case
[simply obtained by solving the quadratic (disper)] for the particular
value $x_=0.05$. This figure shows the presence of unstable
modes within the range of values for $$ that we take to
be physically realistic prix}: $0.4   0.7$.
From this figure we immediately deduce two things. First, we see that the
unstable modes indeed satisfy the criterion (yrange).
Secondly, the unstable modes may have imaginary parts as
large as Im~$  0.15$. It is useful to
ask what this implies for the growth time of the instability.
Since our results only depend on the azimuthal index $m$
through the scaling

$$

Im }  = m _  Im }

$$

we see that the fastest growth time corresponds to the $m=l$ modes.
The e-folding time for the instability follows from

$$

t_e =  { 1  m _  Im } }=
{ 1  2  m  Im }  P  s}

$$

where $P$ represents the observed rotation period of the pulsar
(presumably corresponding to the rotation of the charged component, i.e.
$P/2/_$).
figure}

[height=6cm,clip]{shell_2.eps}
Instability regions for the shell problem. We show
results for $l=2$ and relative rotation such that
the neutrons rotate 90\% slower (left frame) or faster (right frame)
than the protons. The two-stream instability operates in
regions 1-2. The grey box corresponds to the ``physically reasonable''
part of parameter space (for the core of a neutron star).}

figure}
figure}

[height=6cm,clip]{rotfreq_2.eps}
Real and imaginary parts (left and right frame, respectively)
of the mode frequencies for $l=2$, $=1.9$ and $x_=0.05$. The
  corresponding instability region can be deduced from the
right panel  of Fig.~shell. The grey area in the left frame indicates the region
where an instability is permissible according to (yrange).
}

figure}
The above example shows that the two-stream instability
does indeed operate in this shell problem.
In fact, the analysis goes beyond the local analysis
of the plane parallel problem in Section~IIB since we have
now solved for the actual unstable modes (satisfying the
relevant boundary conditions). We see that, as expected for a dynamical instability,
the growth time of an unstable mode may be very short.
However, the relative rotation rates required to make
the quadrupole modes unstable in the range $0<x_<1$ and
$0<<1$ are likely far too large to be physically
attainable. In this sense the results shown in Figs.~shell--rotfreq
are, despite being instructive, somewhat extreme.

### A realistic mechanism for triggering pulsar glitches?

A quantity of key importance for this discussion is the
rotational lag between the two components. In order to be able to argue
that the two-stream instability is relevant for pulsar  glitches
we need to
consider lags that may actually occur in astrophysical
neutron stars. To estimate the size of the rotational lag required
to ``explain'' the observed glitches we assume
 that a glitch  corresponds to a transfer of
angular momentum from a partially decoupled superfluid component
(index $$) to the bulk of the star (index $$). Then we have

$$

I_ | _|  I_  _
  _  { I_  I_ | _|

$$

where $I_X$ are the two moments of inertia. Now assume that the
decoupled component corresponds 1\% of the total moment of inertia, eg.
the superfluid neutrons in the
inner crust or a corresponding amount of fluid in the core.
This would mean that $I_  10^{-2} I_$, and we have

$$

 _  10^{-2} | _| \ .

$$

Combine this with the
observations of large Vela glitches to get

$$

{  _  _  10^{-2} { | _|
 _  10^{-6} \ .

$$

In other words, we must have

$$

| _|  10^{-4} _ \ .

$$

If we assume that the glitch brings the two fluids back into
co-rotation, then we have $ _ = _-_ =  $
and we see that the two rotation rates will
maximally differ by one part in $10^4$ or so. Rotational lags of this
order of magnitude have often been discussed in the context of glitches.
Even though the key quantity in models invoking catastrophic
vortex unpinning in the inner crust --- the pinning strength --- is very uncertain,
and there have been suggestions that the pinning force is too weak
to allow a build up of the required rotational lag jones}, typical values
considered are consistent with our rough estimate.
In addition, frictional heating due to a difference in the
rotation rates of the bulk of a neutron star and a superfluid component
has been discussed as a possible explanation for the fact that
old isolated pulsars seem to be somewhat hotter than expected from standard
cooling models friction1,friction2}.  friction2}
argue that a lag of

$$

{   _   (3.210^{-4}-9.5 10^{-3})
(0.1 s}  P )

$$

could explain the observational data.
Finally, the presence of rotational lags of the proposed magnitude is supported
by a statistical analysis of 48 glitches in 18 pulsars lyne}. This study
suggests that the critical rotational lag at which a glitch occurs is

$$

{    _  5  10^{-4} \ .

$$

In order to make our shell model problem more realistic we
 consider the  case when the superfluid neutrons
lag behind the superconducting protons,  and  take
$  /_ = 5 10^{-4}$, or $ = 1.0005$, as a
 representative value. With this rotational lag, we see from
 (yrange) that the unstable modes must be such that
$-1.0005 <  < -1$.
A series of results for this choice of parameters
are shown in Figures~rotdomain-imag25.
Figure~rotdomain illustrates the fact that, if we
decrease the rotational lag then the two-stream instability
will not be active (in the interesting region of
parameter space) for low values of $l$.
For a smaller rotational lag the instability
acts on a shorter length scale. For $ = 1.0005$ we find that
we must have $l>65$ in order for there to be a region of instability
in the part of the $x_-$ plane shown in
Figure~rotdomain. This means that the instability
only operates on length scales shorter than $ R/l  500 $~m
(if we take the shell radius to be $R=10$~km).
figure}

[height=8cm,clip]{rotdomain.eps}
 The two-stream instability regions (labeled 1 and 2)
for the case when the
superfluid neutrons lag behind the superconducting protons
in such a way that $  /_
= 5 10^{-4}$ or $ = 1.0005$. We show results for
four different values of $l$. There are no unstable
modes in this part of parameter space unless $l>65$. Recall that
$x_<0.1$ and $0.4   0.7$ would be reasonable parameter
values for a neutron star core. The grey diagonal line represents the
singularity discussed in Section~IIID and the dashed curves indicate the
instability regions in the large $l$ limit.}
 
figure}
Figure~freq25 shows the real part of the mode frequencies
for $l=100$ and various values of $x_$. From this figure we can see that
the instability always occur in the region suggested by the
instability condition (yrange), i.e. two real frequency modes never merge
to give rise to a complex conjugate pair of solutions outside the grey areas
indicated in  the various panels of Figure~freq25.
The imaginary parts for $l=100$ and the various values of $x_$
considered in Figure~freq25
are shown in Figure~imag25.
From this figure we see that the imaginary part of $$ typically reaches
values of order $10^{-4}$. In fact,
by comparing similar results for different values of $l$
we have found that the largest attainable imaginary part of $$ varies
by less than one order of magnitude as $l$ increases from
100 to 1000. Thus we estimate that the typical instability growth time
for $=1.0005$  will be

$$

t_e  { 10^4  m } { P  2  s} \ .

$$

For a star rotating at the rate of the Vela pulsar, $P= 89$~ms,
we would have  $t_e  1.4$~s for $l=m=100$.
Interestingly,  this predicted growth time is significantly
shorter than the resolved rise time of a large Vela glitch
$t_{ glitch}< 40$~s velarise}.
figure}

[height=8cm,clip]{freq_l_100.eps}
Mode frequencies (represented by
Re~$$) as function of the entrainment parameter $$
for $l=100$,  $=1.0005$ and various
values of $x_$. The range in which an instability is permissible
[according to (yrange)]
is indicated by the grey areas.}

figure}
figure}

[height=6cm,clip]{freq_im_l_100.eps}
The imaginary part Im~$$ (determining the growth rate)
of the unstable modes for
$=1.0005$ and $l=100$ is shown as a function of $$
for several different values of $x_$ (as indicated in the figure).
Essentially, these results represent
horizontal cuts through the frames in Figure~rotdomain.  }

figure}

### Approximate results: The large $l$ limit

The results obtained above indicate that the two-stream instability
is likely to act on modes with rather short wavelengths. Given this
it makes sense to consider the large $l$ limit
in more detail. Keeping only the leading order term (proportional to $l^4$)
in (disper)
we have the dispersion relation

$$

(1--x_)^2  & +&
[ 1-2-x_+2x_  + (1-x_-2x_ )]  \\
&+&
(1-2-x_) + x_ + (1-x_)^2-2x_^2(1-)^2 =0 \ .

$$

We can readily write down the solutions to this quadratic:

$$

_ &=& { 1  2(1-x_-)} \{ 1-2-x_+2 x_
+(1-x_-2x_ )  .  \\
& & . (1-) [(1-2)(1-2-x_)(1-x_-2 x_) ]^{1/2}
\} \ .

$$

It turns out that we can learn a lot about the problem from this
expression. The most obvious feature is the fact that
$_$ have a singularity when $1-x_-=0$.
It is straightforward to show that one of the roots will become infinite
at this point, while the second root becomes:

$$

 = { 1  1-2 x_ [  - x_(1+)+2x_  (1-) ] \ .

$$

For the examples shown in Figure~rotdomain
this special case corresponds to the intersection between
the instability domain and the
diagonal line $1-x_-=0$, as  indicated in
Figure~rotdomain.
It is also straightforward to deduce the regions of instability from
the sign of the argument of the square-root. We see that we will have
an unstable mode when

$$

<{ 1 2}  and}  1-2<x_<{ 1  1+2
 Region 1}
$$

or

$$

>{ 1 2}  and}  x_>{ 1  1+2
 Region 2} \ .

$$

These regions are also indicated in Figure~rotdomain.
Out of these two possible instability regions, the first is  most likely to
be relevant for neutron stars since it allows the instability to be present
already for small proton fractions.
Finally, we can  use (kappas) to show the existence of an extremum at
displaymath}
 = { 1  8} ( 17}-1) 0.39  \ ,  x_ =
{ 1 4} {17}+7  17}+3}  0.39 \ .
displaymath}
The corresponding imaginary part of $$ would represent
the fastest possible growth time for an unstable mode located in
region~1 of Figure~rotdomain. This leads to the estimate

$$

Im }  0.24 (-1)

$$

or an estimate of the shortest growth time:

$$

t  { 6.7 10^{-2} l} ( {    _ )^{-1}
({ P  0.1  s}} )  s}

$$

which agrees well with the result we previously obtained for $l=m=100$.
Hence, this simple formula can be used to estimate  the
fastest growth rate of the two-stream instability in our shell model
for different parameter values.

## Discussion

In this paper we have introduced the superfluid two-stream instability:
A dynamical instability analogous to that known
to operate in plasmas anderson}, which sets in once the relative
flow between the two components of the system reaches a critical level.
We have studied this instability for two different model problems.
First we analysed a local dispersion relation derived for the case of a background
such that one fluid was at rest while the other had a constant flow rate.
This provided a proof of principle of the existence of the two-stream
instability for superfluids. Our analysis was based on the two-fluid equations
that have been used to model the dynamics of the outer core of a neutron
star, where superfluid neutrons are expected to coexist with superconducting
protons and relativistic electrons. These equations are analogous to the
Landau model for superfluid Helium~Even though we do not discuss this
issue in detail here, it is exciting to contemplate possible experimental
verification of the superfluid two-stream instability in, for example,
superfluid $^4$He.}, and should also (after some modifications
to incorporate elasticity and possible vortex pinning) be relevant
for the conditions in the inner crust of a mature neutron star.
Thus we expect the two-stream instability to be generic in dynamical
superfluids, possibly limiting the relative flow rates of
any multi-fluid system. Our second model problem concerned two fluids
confined within an infinitesimally thin spherical shell.
The aim of this model was to assess whether
the two-stream instability may be relevant (perhaps as trigger mechanism)
for pulsar glitches. The results for this problem demonstrated
that the entrainment
effect could provide a sufficiently strong coupling for the instability
to set in at a relative flow small enough to be astrophysically
plausible. Incidentally, the modes
that become dynamically unstable in this problem are the superfluid analogues of the
inertial r-modes of a rotating single fluid star. This is interesting
since the r-modes are known to be secularly unstable due to the emission
of gravitational radiation~r_rev}. In fact, the connection between the two
instabilities goes even deeper than this since the radiation-driven secular
instability is also a variation of the Kelvin-Helmholtz instability.
In that case, the two fluids are the stellar fluid and the radiation.
In order for an instability to be relevant
the unstable mode must grow faster than all
dissipation timescales. In the case of a superfluid
neutron star core the main dissipation mechanisms are
likely to be mutual friction and ``standard'' shear viscosity
due to electron-electron scattering. Since we have tried to
build a plausible case for the two-stream instability to
be relevant for pulsar glitches we would like to obtain some
rough estimates of the associated dissipation timescales.
To do this we first use
an estimate of when mutual friction is likely to dominate
the shear viscosity [due to  mendell2}]:

$$

 > 100 ( {10^6  cm}  )^2 ({T  10^7 K}} )^2
s}^{-1}  100 ( {l  )^2 ({T  10^7 K}} )^2
s}^{-1}

$$

where we assume that the wavelength of the mode is $ =  R /l$. We can write this as

$$

P < 0.62 l^{-2}({T  10^7 K}} )^2    s}

$$

which suggests that the shear viscosity will be the dominant
dissipation mechanism for large values of $l$.
For example, for a neutron star rotating with the period of the Vela pulsar
mutual friction would dominate for $l<15$ or so (assuming $T_7 5$).
To estimate the shear viscosity damping we can use results obtained for the
secular r-mode instability. In particular,
ksteg} have shown that for a uniform density star
one has

$$

t_{sv}  { 3  4(l-1)(2l+3) } { M   R} 
{ 3  8 l^2}  { M   R} \ .

$$

If we use the shear viscosity coefficient for electron-electron scattering

$$

_{  6 10^{18} ( {  10^{15}  g/cm}^3} )^2
({ 10^9 K}  T} )^2   g/cm s}
 2.7 10^{18} ( { M 1.4 M_ )^2
({10  km}  R})^{6}({ 10^9 K}  T} )^2    g/cm s}

$$

we get

$$

t_{sv}   { 1.210^4  l^2 } ( { 1.4 M_  M )
({R  10  km} })^{5}({T  10^7 K}} )^2   s}

$$

We want to compare this damping timescale to the growth rate of the unstable modes
in our shell toy-model. Combining (growth) with (tsv) we estimate that in order
to have an instability we must have

$$

l < 90 ( {  / _  510^{-4}})
({ 0.1  s}  P} )
( { 1.4 M_  M )
({R  10  km} })^{5} ({T  10^7 K}} )^2 \ .

$$

Let us now consider the case of the Vela pulsar.
Estimating the core temperature as $5 10^7$~K [roughly two orders of
magnitude higher than the observed surface temperature page}] we deduce that only modes
with $l>2500 $ or so are likely to be stabilized by shear viscosity.
Given that our results indicate that the two-stream instability
is active for much smaller values of $l$, cf. the results shown in Figure~rotdomain,
we conclude the dissipation is unlikely to suppress the
instability in sufficiently young neutron stars.
Incidentally, the length scale corresponding to a mode with $l=2500$
would be about ten meters.
This is an interesting result since one can show that a
large glitch could be explained by a small fraction ($ 10^{-4}$)
of the neutron vortices moving a few tens of metres cordes}.
Obviously, the situation changes as
the star cools further. Based on the above estimates one can show that
shear viscosity will suppress all modes with $l>65$ (i.e. all unstable modes
for the case considered in Fig.~rotdomain) if
the core temperature is below $8 10^6$~K.
This means that the two-stream instability may not be able to overcome the
viscous damping in a sufficiently cold neutron star, which is
consistent with the absence of glitches in mature pulsars.
We believe that
the results of this paper suggest that the superfluid two-stream
instability may be relevant in the context of pulsar
glitches. If this is, indeed, the case then what is its exact role?
The answer to this question obviously requires much further work, but
it is nevertheless interesting to speculate about some possibilities.
Most standard models for glitches are based on the idea of catastrophic
vortex unpinning in the inner crust ai}. This is an attractive
idea since the glitch relaxation (on a timescale of days to months) would
seem to be well described by vortex creep models vcreep}.
An interesting scenario is provided by the thermally induced glitch model
 discussed by link1}. They have
shown that the deposit of $10^{42}$~erg of heat would be sufficient
to induce a Vela type glitch.
The mechanism that leads to the unpinning of vortices, eg. by the deposit
of heat in the crust, is however not identified. We
believe that the two-stream instability may fill this gap
in the current theory.
It should, of course, be pointed out that glitches need not originate in
the inner crust. In particular,  jones}
has argued that the vortex pinning
is too weak to explain the recurrent Vela glitches. If this argument
is correct then the glitches must be due to some mechanism operating in the
core fluid. Since the model problems we have considered would be relevant for
the conditions expected to prevail in the outer core of a mature neutron star,
our results show that the two-stream instability may serve as a trigger
for glitches originating there. The key requirement for the
instability to operate is the presence of a rotational lag.
It is worth pointing out that such a lag will build up both when there
is a strong coupling between the two fluids (i.e. when the vortices are pinned)
and when this coupling is weak. One would generally expect the strength
of this coupling to vary considerably at various depths in the star langlois}, and it
is not yet clear to what extent a rotational lag can build up
in various regions. This is, of course, a key issue for  future
theoretical work on pulsar glitches.
One final relevant point concerns the recent observation of a
Vela size glitch in the anomalous X-ray pulsar
1RXS J170849.0-400910 kaspi}. This object
has a spin period of 11~s, which means that any
feasible glitch model must not rely on the star
being rapidly rotating. What does this mean for our proposal
that the two-stream instability may induce a glitch?
Let us assume that the  rotational lag builds up at the same rate as the
electromagnetic spindown of the main part of the star (i.e. that
the superfluid component does not change its spin rate at all
under normal circumstances).
Then the lag would be $   t $ after time $t$.
If there is a critical value at which a glitch will happen (corresponding to
$ _{ crit}$) then the interglitch time $t_g$ could be
approximated by
$$
t_g  {  _{ crit}   } {   } =
2 {  _{ crit}   }
$$
where $$ is the standard ``pulsar age''. This argument implies the following:
i) For $  _{ crit} /  510^{-4}$
we would get $t_g  10^{-3} $. This (roughly) means that only pulsars younger than
 $10^4$~yr would be seen to glitch during 30 years of observation,
which accords well with the fact that only young pulsars are
active in this sense. ii) There is no restriction on the rotation rate in this
scenario; a star spinning slowly may well exhibit a glitch as long as
its spindown rate is fast enough. This means that one should not
be surprised to find glitches in stars with
extreme magnetic fields (magnetars).
This paper is only a first probe into what promises to
be a rich problem area. Future studies must address issues concerning
the effects of different dissipation mechanisms, the nonlinear evolution
of the instability, possible experimental verification for superfluid
Helium etcetera. These are all very interesting problems which we
hope to investigate in the near future.

## Acknowledgements

NA and RP acknowledge support from the EU
Programme 'Improving the Human Research Potential and the Socio-Economic
Knowledge Base' (Research Training Network Contract HPRN-CT-2000-00137).
NA acknowledges support from the Leverhulme Trust in the form of a prize
fellowship, as well as generous hospitality offered by the Center for
Gravitational-Wave Phenomenology at Penn State University.
GC acknowledges partial support from NSF grant PHY-0140138.
thebibliography}{12}
[Anderson et al}{2001}]{anderson}
Anderson, D., R. Fedele and M. Lisak, Am. J. Phys. 69, 1262 (2001)
[Anderson \& Itoh}{1975}]{ai}
Anderson, P.W., and N. Itoh, Nature  256, 25 (1975)
[Andersson \& Comer}{2001}]{ac01}
Andersson, N., and G.L. Comer, MNRAS 328, 1129  (2001)
[Andersson et al}{2002}]{inert2}
Andersson, N., G.L. Comer and R. Prix, { The inertial
  modes of rotating superfluid neutron stars}, manuscript in preparation
[Andersson \& Kokkotas}{2001}]{r_rev}
Andersson, N., and K.D. Kokkotas, Int. J. Mod. Phys. D  10, 381 (2001)
[Baym et al}{1969}]{bppr}
Baym, G., C. Pethick, D. Pines and M. Ruderman, Nature, 224,
872 (1969)
[Blaauwgeers et al}{2001}]{kh}
Blaauwgeers, R.,  et al { Shear flow and Kelvin-Helmholtz instability in
superfluids} preprint cond-mat/0111343
[Buneman}{1963}]{buneman}
Buneman, O., Phys. Rev. Lett. 10, 285, (1963)
[Buneman}{1959}]{buneman2}
Buneman, O., Phys. Rev. 115, 503, (1959)
[Casti et al}{1998}]{casti}
Casti, A.R.R., P.J. Morrison and E.A. Spiegel,
Negative energy modes of gravitational instability of interpenetrating fluids,
preprint astro-ph/9807310
[Cheng \& Ruderman}{1977}]{pulsar1}
Cheng, A.F., and M.A. Ruderman, Ap. J. 212, 800 (1977)
[Cheng et al}{1988}]{vcreep}
Cheng, K.S., M.A. Alpar, D. Pines and J. Shaham, Ap. J.  330, 835
(1988)
[Cordes et al}{1988}]{cordes}
Cordes, J.M., G.S. Downs and J. Krause-Postorff, Ap. J. 330, 847 (1988)
[Dodson et al}{2002}]{velarise}
Dodson, R.G., P.M. McCullogh and D.R. Lewis, Ap. J. Lett.  564,
85 (2002)
[Drazin \& Reid}{1981}]{drazin}
Drazin, P.G., and W.H. Reid, Hydrodynamic stability (Cambridge Univ.
Press, New York 1981)
[Farley}{1963}]{farley}
Farley, D.T., Phys. Rev. Lett. 10, 279 (1963)
[Jones}{1998}]{jones}
Jones, P.B., MNRAS 296, 217 (1998)
[Kaspi et al}{2000}]{kaspi}
Kaspi, V.M., J.R. Lackey and D. Chakrabarty, Ap. J. Lett. 537, 31 (2000)
[Kokkotas \& Stergioulas}{1999}]{ksteg}
Kokkotas, K.D., and N. Stergioulas, Astron. Astrophys.  341, 110 (1999)
[Langlois et al}{1998}]{langlois}
Langlois, D., D.M. Sedrakian and B. Carter, MNRAS  297, 1189 (1998)
[Larson \& Link}{1999}]{friction2}
Larson, M.B., and B. Link, Ap. J. 521, 271 (1999)
[Link \& Epstein}{1996}]{link1}
Link, B., and R.I. Epstein, Ap. J. 457, 844 (1996)
[Lovelace et al}{1997}]{galax}
Lovelace, R.V.E., K.P. Jore and M.P. Haynes, Ap. J. 475, 83 (1997)
[Lyne et al}{2000}]{lyne}
Lyne, A.G., S.L. Shemar and F. Graham Smith, MNRAS  315, 534 (2000)
[Lyubarsky}{2002}]{pulsar3}
Lyubarsky, Y.E., { Coherent radio emission from pulsars} preprint
astro-ph/0208566
[Mendell}{1991a}]{mendell1}
Mendell, G.L., Ap. J. 380, 515 (1991)
[Mendell}{1991b}]{mendell2}
Mendell, G.L., Ap. J. 380, 530 (1991)
[Page}{1997}]{page}
Page, D., Thermal evolution of isolated neutron stars, p. 539 in
The many faces of neutron stars, Ed: R. Buccheri, J. van Paradijs and
M.A. Alpar (Kluwer, Boston 1998)
[Papaloizou \& Pringle}{1978}]{pandp}
Papaloizou, J.C.B., and J.E. Pringle, MNRAS  182 423 (1978)
[Pierce}{1974}]{pierce}
Pierce, J.R., Almost all about waves (MIT Press, Cambridge MA 1974)
[Prakash et al}{1988}]{PAL88}
Prakash, M., T.L. Ainsworth and J.M. Lattimer, Phys. Rev. Lett. 61, 2518 (1988)
[Prix}{2002}]{prix02}
Prix, R., { Variational derivation of Newtonian multi-fluid hydrodynamics}
preprint physics/0209024
[Prix et al}{2002}]{prix}
Prix, R.,  G.L. Comer and N. Andersson,
Astron. Astrophys.  381, 178 (2002)
[Prix \& Rieutord}{2002}]{pr02}
Prix, R., and M. Rieutord, Astron. Astrophys. 393, 949 (2002)
[Provost et al}{1981}]{provost}
Provost, J., G. Berthomieu and A. Rocca, Astron. Astrophys.  94 126 (1981)
[Radakrishnan \& Manchester}{1969}]{vela1}
Radakrishnan, V., and R.N. Manchester, Nature  222, 228 (1969)
[Reichley \& Downs}{1969}]{vela2}
Reichley, P.E., and G.S. Downs, Nature  222, 229 (1969)
[Ruderman}{1969}]{ruder}
Ruderman, M., Nature 223, 597 (1969)
[Shapiro \& Teukolsky}{1983}]{shapiro}
Shapiro, S.L., and S.A. Teukolsky, { Black holes, white
dwarfs and neutron stars} (Wiley 1983)
[Shibazaki \& Lamb}{1989}]{friction1}
Shibazaki, N., and F.K. Lamb, Ap. J. 346, 808 (1989)
[Weatherall}{1994}]{pulsar2}
Weatherall, J.C.,  Ap. J.  428, 261 (1994)
thebibliography}
