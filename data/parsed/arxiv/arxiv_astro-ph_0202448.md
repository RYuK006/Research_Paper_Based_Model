---
paper_id: "arxiv:astro-ph/0202448"
title: "Phase structure of self-gravitating systems"
authors:
  - Victor Laliena
year: 2004
doi: "10.1016/j.nuclphysb.2004.02.027"
source: "arxiv"
parser_used: "arxiv_latex"
parsed_at: "2026-11-09T05:09:01.297788+00:00"
equation_count: 22
table_count: 0
---

# Phase structure of self-gravitating systems

## Abstract

The equilibrium properties of classical self-gravitating systems in the grand canonical ensemble are studied by using the correspondence with an euclidean field theory with infrared and ultraviolet cutoffs. It is shown that the system developes a first order phase transition between a low and a high density regime. In addition, due to the long range of the gravitational potential, the system is close to criticality within each phase, with the exponents of mean field theory. The coexistence of a sharp first order transition and critical behavior can explain both the presence of voids in large regions of the universe as well as the self-similar density correlations in terms of self-gravity alone.

## Document Content

{footnote}}
center}
** Phase structure of self-gravitating systems** \\
0.5truecm}
Victor Laliena \\
0.25truecm}
{
*Departamento de F\'{sica Te\'orica, Universidad de
Zaragoza, \\
Pedro Cerbuna 12, E-50009 Zaragoza (Spain)
\\
0.15truecm}
laliena@unizar.es \\
}}
0.25truecm}
January 16, 2003
center}
1truecm}
center}
**Abstract**
center}

The equilibrium properties of classical self-gravitating systems in
the grand canonical ensemble are studied by
using the correspondence with an euclidean field theory with
infrared and ultraviolet cutoffs.
It is shown that the system
develops a first order phase transition between a low and a high
density regime. In addition, due to the long range of the
gravitational potential, the system is close to criticality within
each phase, with the exponents of mean field theory.
The coexistence of a sharp first order transition and critical
behavior can explain both the presence of voids in large regions of the
universe as well as the self-similar density correlations
in terms of self-gravity alone.
0.5truecm}
{

*Keywords*: Field Theory; Critical Phenomena; Long Range Forces \\
0.15truecm}

PACS: 11.10.-z, 64.60.-i, 05.20.-y
}

{footnote}}
footnote}{0}

##  1 \ Introduction

One of the outstanding problems of modern cosmology is the
understanding of structure formation in the universe [peebles93].
Visible matter at astronomical scales appears organized in a hierarchy of
galaxies, cluster and supercluster of galaxies, which tend to be
found in filamentary aggregates or two-dimensional sheets that
encompass large regions with much lower density of matter and
structures. These regions, called voids,
occupy a large fraction of the observed universe, and are also organized in a
hierarchy [einasto1,einasto2].
The theoretical investigation of void formation
is receiving increasingly attention [peebles01].
There is general agreement that the galaxy two point correlation
function is scale invariant (self-similar), at least at not too
large scales, decaying as
a power of the distance, $1/r^$.
The exponent $$ as well as the scale
of homogeneity is still controversial. Pietronero and coworkers
found $ 1$ and claim that the power law is obeyed up to
the deepest distances [pietronero]. Other authors gave a different
exponent ($ 1.8$) and support the existence of an observed
scale of homogeneity
[nonfractal:davis,nonfractal:peebles,nonfractal:guzzo].
Self-similar behaviour has also been found in the interstellar medium
[ism:larson,ism:hetem,ism:kramer,ism:stutzki].
Although certainly the dynamics must be very important in order to explain
these facts, and many physical effects might play a prominent role,
it is well possible that many aspects of the observed structures may
be understood in terms of the equilibrium states of self-gravitating
matter alone, as claimed by the authors of Refs. [dvsc,pm].
Indeed, it has been tried to apply thermodynamics to astrophysical systems
since a long time (see for instance Ref. [saslaw]).
In this paper, we will analyze the general phase structure of a
non-relativistic self-gravitating system at thermal equilibrium.
The results are general and can be applied to any such system that can be
considered to be in these conditions. We will not be concerned here with the
very interesting questions of whether thermal equilibrium  can be reached in
such systems, or the way it is attained. We just assume that the
self-gravitating system is at thermal equilibrium.
Let us consider a system of $N$ classical particles of mass $m$ confined
in a region of volume $V$ and
interacting each other via the Newtonian gravitational potential.
Its hamiltonian reads

$$

{ H}\;=\;1}{2m}\,_{i=1}^N _i^2-\:G m^2}{2}\,
_{i j} 1}{|_i-_j|} \, . 

$$

The thermodynamics of such a system is ill defined: the entropy
does not exist due to the singularity of the potential at short
distances [pad,eduardo].
Furthermore, even if one modifies the potential
to remove the short distance singularity, the usual thermodynamical
limit does not exist, since the thermodynamic potentials are not extensive,
due to the long range gravitational force.
In such cases, the microcanonical specific
heat can become negative and different statistical
ensembles are not equivalent (see Refs.
[gross,lynden-bell,thirring,stahl,torcini,chav:som,youngkins,ispolatov,chavanis,chav:isp]).
In particular, the grand canonical ensemble
is dominated by completely collapsed configurations, whatever the chemical
potential.
To use the ordinary thermodynamical tools, the potential must also be
modified at long distancesIt has been proposed
that a kind of thermodynamical limit for systems with potentials decaying
as $1/r$ could be taken by considering the so called
dilute regime [devega], but it can be shown that this statement
cannot hold [victor2].}.
The thermodynamics of self-gravitating system has been studied since a
long time by confining a finite system on a finite box and using
mean field theory.
The approach developed in this paper is different: we will
describe the thermodynamical
properties of a self-gravitating system as the limiting case of a
family of well behaved, short range systems, the interactions of which
decay with distance more and more slowly, thus resembling more and more
the newtonian $1/r$ potential. For these systems the usual thermodynamical
limit, which is considered in this paper, does exist.
To carry out this investigation, we will take advantage of the fact that
the statistics of a self-gravitating ensemble of particles can be related
to an euclidean field theory of a single scalar field [dvsc,pm],
in a similar way to the relation between the Coulomb gas and the
Sine-Gordon field
theory [coulomb:froelich,coulomb:polyakov,coulomb:samuel].
Hence, the remaining of the paper will rely on the techniques of
euclidean field theory.

##  2 \ Field theoretical description of a self-gravitating
system

The statistical mechanics of a self-gravitating system can be studied
in the usual way if the gravitational potential is regularized at short
and long distances.
Let us choose as a regularized gravitational potential,
denoted by $(r)$,
an attractive Yukawa potential, with range $1/m_0$, endowed
with a hard core of size $r_0$ at short distances: $(r)=
-Gm^2 e^{-m_0 r}/r$ for $r>r_0$
and $(r)=$ for $r<r_0$.
After integrating out the momenta, the grand canonical partition
function for chemical potential $$
and temperature $T$ can be written as

$$

{ Z}_{ GC}}=_N \, e^{ N}\,
(m a^2}{2^2})^{3N/2}
 Z}_N\, ,

$$

where
$=1/k_BT$, $a$ is a constant with units of length, to
be specified below, and

$$

 Z}_N=a^{-3N}}{N!}
_{i=1}^Nd^3r_i\,\{-{2}
_{i j}(|_i-_j|)\} \, .

$$

The partition function $ Z}_N$ can be approximated by
dividing the space volume in $=V/a^3$ cells of size $a$ (the
unit length introduced above),  and replacing
the integrals by appropriate Riemann sums, which can be reorganized as a
sum over cell occupation numbers $S_i$, with the index $i$ running from
$1$ to the number of cells, $$. If $a$ is of the order of the
hard core size, each cell can be either void or occupied by one particle:
$S_i=0,1$. This is similar to consider self-gravitating
fermions [chavanis]. We get

$$

 Z}_N \,=\, _{S_1=0}^1_{S_{=0}^1
\,\{b^2}{2}[_{n,n'}\,
U_{ L}}(n-n')
S_n S_{n'}-U_{ L}}(0) N ]\} \:
(_n S_n - N) \, ,

$$

where $b^2=4  G m^2$,  $U_{ L}}(n-n')$}
is a proper lattice version of
$-(-')/(4 G m^2)$,
the factor $1/N!$ has been canceled due to the distinguishability
of classical
particles, and the Kronecker delta takes into account that the number
of particles is fixed [victor].
Since the Yukawa potential is the Green function of
$-^2+m_0^2$,
we can choose its lattice version as the lattice Green function
of $-_{ L}}^2+m_0^2$, where
$_{ L}}^2$ is a discretization of the
laplacian:

$$

U_{ L}}(n-n')\;=\;1}{a^3}\,
(1}{-^2_{ L}}+m_0^2})_{n,n'}\, .

$$

Using (latpot) and the Hubbard-Stratonovich
formula, we can write the following identity:

$$

&&\{b^2}{2}_{n,n'}\,U_{ L}}(n-n') S_n
S_{n'}\} \;=  \\
&& \;\;\;\;\;\;
C\,\,[d]\,\{-1}{2}\,_{n,n'}\,a^3\,
_n\,(-^2_{ L}}+m_0^2)_{nn'}\,_{n'}\:+\:
b\,_n_n S_n\} \, ,

$$

where $C$ is a number independent of $S_n$. Plugging Eq. (hs) in
(discpf) and the resulting equation for $ Z}_N$ in the
expression for $Z}_{ GC}}$, and performing the summation
over $S_i$, we can write
the grand canonical partition function of
the (regularized) self-gravitating system in terms of a local euclidean field
theory with a single scalar field $_n$:

$$

{ Z}_{ GC}}=C[d][-{ S}]\, ,

$$

the action of which is given by

$$

{ S}=1}{2}_{nn'}a^3
_n{ D}_{nn'}_{n'}-
_n (1+g  e^{b_n})\, ,

$$

where $g= e^{ e^{-b^2}{2}U_{ L}}(0)}
(m a^2}{2^2})^{3/2}$ and
${ D}=-^2_{ L}}+m_0^2$.
Notice the unusual form of the action: the
interaction term, $(1+g e^{b)$, is unbounded from
below. It behaves as $-b$ for $$. The action,
however, is bounded from below if $m^2_0>0$. This reflects the fact
that the grand canonical ensemble does not exist for non-extensive
(long range and/or purely attractive) systems. The infrared and
ultraviolet cutoffs, $m_0$ and $a$ respectively, make the system
short ranged and repulsive at short distances (hard core of size
of the order of $a$), and thermodynamics is well defined.
In the naive continuum limit, in which
$a 0$ ($g 0$)
and the relevant field configurations are smooth,
we recover the action of Ref. [dvsc]. This continuum action is not
bounded from below and hence the corresponding functional integral
diverges. Thus, the results of Ref. [dvsc] are at most formal
and the conclusions different from ours. The regulators, $a$ and $m_0$,
play an essential role, although the conclusions, as we will see,
are independent of them (provided they are small enough).
The action contains four parameters: the lattice spacing, $a$, which
obviously has dimension of length; the inverse of the potential range,
$m_0$, which has dimension of $(length})^{-1}$; $b$, with
dimension of $(length})^{1/2}$; and $g$, which is
dimensionless. The field is canonically normalized, so that its
dimension is $(length})^{-1/2}$.
It is convenient to redefine the field such that $_n=b_n+ g$,
and to work in terms of the dimensionless
quantities $=a/b^2$, $=a^2 m_0^2$, and
$h=1/2+ g$. Ignoring constant terms, the action reads

$$

{ S}={2}_{nn'}
_n  D}_{nn'}_{n'}
-_n _n}{2}
-h\,_n_n\, ,

$$

where $ D}=-+$.
An action of the same form, with $=0$, has been obtained in
Ref. [pm] in a similar way. In that case, however,
the parameter $h$ has a different meaning.
Notice that for $h=0$ the action (action) has the symmetry
$_n -_n$. Since the term linear in $_n$
breaks this
symmetry, we will have $>0$ for $h>0$ and
$<0$ for $h<0$. At $h=0$ we will have
$=0$ unless the symmetry is spontaneously broken.
The average of particle and energy densities, $$ and $$,
can be obtained as
derivatives of the grand canonical partition function. This allows
to express them in terms of the field $$ in the following way:

$$

 &=&
1}{V}_n e^{_n}}{1+ e^{_n}}\, ,
 \\*
 &=&
k_B T[3}{2}-1}{2}
1}{V}_n[_n- g-^{-1}D}}^{-1}_{nn}]
 e^{_n}}{1+ e^{_n}}
] \, .

$$

One can easily identify the first contribution to the energy in
Eq.~(energy) as the kinetic energy and the second one as the
potential energy. The later has the form
$_n (_n- g-^{-1}D}}^{-1}_{nn})_n$,
where $_n= e^{_n}/(1+ e^{_n})$ is the local
particle density, what implies that the field
$_n$ represents, up to an additive constant,
$ g+^{-1}D}}^{-1}_{nn}$,
the local gravitational potentialNote that
$D}}^{-1}_{nn}$ is independent of $n$ due to the
translational invariance of the Laplacian.}.
After some algebraic manipulations, which are outlined in the appendix
since they are not completely straightforward, we can write the following
exact equation for the average energy, which has the expected form:

$$

=k_B T[3}{2}-1}{2}1}{V}_n_{r 0}
^{-1}_nD}}^{-1}_{n,n+r}_{n+r}
]\, .

$$

In the above equation $$ and $$ stand for the average energy and
density, respectively. Remember that
$D}}^{-1}_{n,n+r}  e^{-m}_0 r}/r$.
Notices that the fact that the term with $r=0$ is
excluded from the sum over $r$ in Eq.~(avenergy) implies that the
contact term does not contribute to the energy. This, and the bounds
$0<_n<1$, are manifestations of the particle hard core.

##  3 \ Phase diagram

Perturbation theory in euclidean field theory starts by identifying
the minimum of the classical action and assuming that the relevant
field configurations are small fluctuations around this minimum.
For the action (action) this is a good approximation if $$
is large. We shall argue below that it is indeed
a good approximation whatever $$ if $$ is small.
The minimum of the action obviously corresponds to the constant field that
minimizes the classical potential

$$

{ U}\;=\;{2}^2\:-\:
{2}\:-\:h \, ,

$$

and, therefore, satisfies the equation

$$

\;=\;1}{2}\,{2}\:+\:h \, .

$$

figure}[t!]
[width=2.5in,angle=90]{phd.ps}}
Phase diagram in the $(,g)$ plane. The solid
line is a first order transition that ends at the critical point.}

figure}
The above equation has one, two or three solutions, depending on
the values of $$ and $h$. When it has one solution, it
correspond to the global minimum; if there are two solutions,
one is the global minimum and the other one a point of inflection;
three solutions correspond to a local maximum, a local minimum,
and the global minimum. In the last case, the minima can only be
degenerate if $h=0$, and then symmetry implies that
Eq.~(minimum) has either one or three solutions:
for $>1/4$ the only solution is $=0$,
while for $<1/4$ we have two
solutions, $=_0 0$ (with $_0$ positive),
which are the two degenerate
global minima, besides the symmetric solution $=0$, which is a
local maximum. We will denote the two global minima by
$_h=+_0$ and $_l=-_0$.
The densities of each phase are respectively

$$

_l=1}{a^3}\, e^{_l}}{1+ e^{_l}}\, ,
1truecm}
_h=1}{a^3}\, e^{_h}}{1+ e^{_h}}\, .

$$

Hence, the solutions $_l$ and $_h$ describe phases
of low and high density respectively.
The phase diagram in the plane $(,g)$, at the classical
level, is displayed in figure~fig:phd. For $>1/4$, the
transition between the low (small $g$) and high (large $g$)
density regimes is smooth. For
$<1/4$, the low density phase is separated from the
high density phase by a first order transition which takes place
at $=[-1/(2)]$ (i.e., $h=0$).
This first order line ends at
the critical point $_c=1/4$,
$g_c=1/ e^2$ ($h=0$). The order parameters,
$=_h-_l$ and
$=_h-_l$,
vanish at the critical point with the classical (mean field)
exponent $1/2$. This mean field critical behavior is a consequence of the
classical approximation and could be modified by the neglected
fluctuations.
For small $$ and $h=0$, Eq.~(minimum) gives
$_h 1/(2)$,
$a^3 _h 1- e^{-1/(2)}$,
$_l -1/(2)$, and
$a^3 _l e^{-1/(2)}$.
Thus, the low density phase is very dilute, while the high density
phase is extremely dense. Most of the densities (including
presumably those of physical systems) are between $_l$
and $_h$, and they correspond, therefore, to the phase
coexistence region.

##  4 \ Critical behavior and correlations

The corrections to the classical approximation can be obtained
perturbatively, by expanding the action around the corresponding
minimum. For each phase we write
$_n=_h+_n$ and $_n=_l+_n$
respectively, and, ignoring again constant terms, the corresponding
actions can be written as

$$

{ S}\;=\;{2}\,_{nn'}\,_n
 D}_{nn'}_{n'}
\:\:\,_n_n
\:-\:_n\,[1+ ( e^{_n}-1)]
\, ,

$$

where the signs $+$ and $-$ correspond to the low and high density
phases respectively, and
$=1-a^3_h=a^3_l$.
When $$ is very small, $$ is much smaller and the
actions for either phase (action_min) are
very close to the gaussian critical point, $=0$. Therefore,
the classical
approximation we are using is very good. In addition, we have a very
interesting situation: *a very sharp first order transition that
separates two phases which, in turn, are close to criticality*.
Hence, the actions (action_min) produce
a very large correlation length and critical (self-similar) behavior
over a vast range of scales. The question is to which universality
class corresponds such critical behavior. In three dimensions, the
gaussian fixed point is infrared unstable under perturbations of
relevant operators. This means that the critical behavior of actions
defined in the neighborhood of the gaussian fixed point can be
governed by a different (non-gaussian) fixed point. For this
to happen, the couplings of the relevant operators of dimension
larger than one must be of the order of $$.
In our case $$ and we are in the
opposite case: the actions~(action_min) lie very close to the
renormalized trajectory of the gaussian fixed point, given by
$=0$, $>0$. Hence, the critical behavior is governed
by the gaussian fixed point, and thus belongs to the mean field
universality class.
The correlations can be computed to leading order in $$
with good accuracy. For the field we get
$_{_{'}
-_{_{'}
=G(-')$}, with

$$

G(-')\;=\;\,d^3p}{(2)^3}\,
 e^{ i  (-')}}{p^2+\, ,

$$

where we have used the continuum expression since the lattice spacing
is much smaller than the correlation length, $=a/()^{1/2}$.
At large distances, $G()$ decays exponentially as
$(-||/)$, but in a wide range of distances, $a||$,
it is approximately self-similar, $G() 1/||$.
The correlations of the density (density),
$(-')$, have the same long distance behavior as
the correlations of the field.
To leading order in $$ we have:

$$

(-')\;=\;^2\, e^{G(0)}\,
[ e^{G(-')}-1]\, .

$$

For large distances $() G()$, and therefore
the density correlations behave as $1/||$ for $a||$.
Hence, the present approach to self-gravitating systems predicts
that density correlations decay as a power
law with exponent $=1$ over a vast range of scales. Since $$
is proportional to the assumed range of the gravitational interaction,
it is well possible that correlations be self-similar at any
observable scale.
It is worthwhile stressing that the above analysis refers to the
quasi-critical behaviour
of each of the two phases as $ 0$. There is a
true critical point at $_c=1/4$ and $g=1/ e^2$
(or $_c=1/2$). In this case the parameters are not small
and a non-perturbative analysis is required in order to investigate the
nature of its universality class. This critical point might be
relevant at very high temperatures, when $$ is of order one.
A similar analysis can be made for small $$ (strong coupling
regime). The symmetry is broken at the classical level
if $<1/4$. For small $$ and small $$
short wavelength fluctuations cannot induce tunneling between the two
minima since it would imply huge fluctuations of the action, of the order
$1/m}_0^4$. Likewise, long wavelength fluctuations
cannot induce tunneling since the barrier is too high,
of the order of $1/(8)$.
The two minima describe phases of low and high density.
The correlation length on each phase
is of the order of $1/$. Hence, the conclusions are the same
as in the weak coupling regime: an abrupt first order transition
separates the low and high energy phases, and each phase present
critical behaviour of mean field type.

##  5 \ Finite volume effects: the Lane-Emden equation

It might seem paradoxical that the mean field solution is homogeneous,
since it is well known that the usual mean field solutions of self-gravitating
systems present density profiles that depend on the distance to the center
of the system. There is
a simple explanation: since we are looking for the mean field
solution of a short ranged translational invariant system in the
infinite volume limit it is natural that it be homogeneous.
Had we looked for the minimum of the action (firstaction) on a
finite box of size $L$ we would have
obtained the equation

$$

_{n'}(-_L^2)_{nn'} _{n'}\:+\:m_0^2_n\:-\:
b g e^{b_n}}{1+g e^{b_n}} \;=\;0\, .

$$

On a finite volume, the walls break translational invariance and
the solution of Eq.~(finite) will not be homogeneous, due to the
boundary conditions imposed to the operator $(-_L^2)_{nn'}$.
Since this operator is a discretization of the Laplacian, if
$L  1/m_0$, Eq.~(finite) is similar to the isothermal Lane-Emden
equation [emden,chandra]
(if $m_0=0$, to leading order in $g$
we will have exactly the discretized Lane-Emden equation, and the
corrections in $g$ are due to the cut-off $a$),
and we will get a solution similar
to the known profiles of self-gravitating systems in the mean field
approximation.
On the other hand, if $L 1/m_0$, the spatial dependence of the solution
will be washed out
and we will have the reported constant solutions. However,
the two solutions correspond to extremely high and extremely low densities,
respectively. The system will only be homogeneous at such extreme densities.
For intermediate densities, inhomogeneities will necessarily develop: the
system will be in a mixture of high and low density domains.
This instability as the volume increases had been notice long ago by
Antonov, who found that the solutions of the Lane-Emden equation
ceases to be (local) maxima of the entropy if the size of the box
is larger than $0.335 G M^2/(-E)$, where $M$ is the total mass and $E<0$ the
energy, and the system collapses [antonov]. This was called
the gravothermal catastrophe in Ref. [wood].

##  6 \ Final remarks

In thermal equilibrium, a self-gravitating system is made up
of domains of low and high density (voids and clusters).
The distribution of domains is a dynamical question that
has to do with the way equilibrium is reached.
The correlations within each domain are self-similar on a vast range
of scales, decaying as $1/r$. The transition to
homogeneityThe scale at which the density
fluctuations cease to be self-similar.} [gaite]
would take place on scales comparable to the range
of the gravitational interaction, which may be larger than the
deepest observed distances. A similar behavior (first order phase
transition and self-similar correlations) was found for the
two-dimensional self-gravitating system by using techniques of
conformal field theory [abdalla].
It is straightforward to take into account the cosmic
expansion in a simplified way, as in Refs. [pm,dvsc], by introducing
comoving coordinates $$ in (hamil), such that the physical
coordinates are $=R(t)$, where $R(t)$ is the scale factor.
As intuitively expected, this is equivalent to rescale the lattice spacing:
$a(t)=R(t) a$ and, consequently, we have the following rescaling of
parameters:
$ R(t)$ and $ R^2(t)$.
This variation of the parameters implies that the difference between
the densities of the two phases decreases. This is not surprising:
the expansion of the universe acts as a pressure that competes with
the tendency of gravity towards collapse.
It is remarkable that the picture of the self-gravitating system
devised in this work is strikingly similar to the observed universe,
despite it is not at thermal equilibrium. The scaling exponent
of the the correlation function of the density, $=1$,
however, is far from the
widely accepted exponent of the galaxy correlation function,
$ 1.8$ for distances between 0.2 and 20 Mpc [peebles93].
As mentioned in the introduction, in the last years
there has been a strong debate about the validity of this result.
Pietronero and his group analyzed the data
from a different perspective and claimed that the exponent of the
galaxy correlation function is $  1$, and that the
self-similar behavior extends up to the deepest explored distances.
The controversy seems not resolved, although most astrophysicist
believe the earlier result, $ 1.8$.
This is theoretically supported by the thermodynamic
arguments given in [saslaw]. These arguments, however, are
somehow heuristic and their validity may be questioned. Indeed, using
Eq.~(avenergy) as starting point,
the same arguments can be applied step by step to the formulation of
the self-gravitating system given in this work, leading to the
same predictions of Saslaw's book. However, the results of this work,
based on a rather rigorous treatment of the self-gravitating system,
are completely different.
Hence, the conclusion of this paper is clear: either Pietronero and
coworkers are right,
and $ 1$, or the thermodynamical approach is not valid
to describe the universe at such scales. The later possibility cannot
be discarded, since it is difficult to argue that the universe is at
thermal equilibrium, and
dynamical effects may play a prominent role in the behavior of
the galaxy correlation function.
In any case, the results obtained in this paper need not be applied to
the universe as a whole, or to the large scale structure of it,
but to any self-gravitating system that are close to
thermal equilibrium. The interstellar gas, where self-similar behavior
has also been observed, might be an instance. In this case the scaling
exponent of the density correlations is compatible with $=1$, but
with large uncertainties [dvsc].
0.25truecm}

*Acknowledgments*
I thank J.L. Alonso, J.L. Cort\'es, and A. Galante for useful
discussions. This work received financial support from Ministerio de
Ciencia y Tecnolog\'{a (Spain) under the Ram\'on y Cajal program,
and from CICyT (Spain) under the project FPA 2000--1252.

##  Appendix

Let us outline in this appendix the derivation of equation~(avenergy),
which is not completely straightforward. The field $_n$ can be obtained
from the derivative of the action as

$$

_n=^{-1}_{n'}D}}^{-1}_{nn'}_{n'}+
^{-1}_{n'}D}}^{-1}_{nn'}
 S}}{_{n'}}
-1/2-h}{\, ,

$$

where we used $_{n'}D}}^{-1}_{nn'}=1/$.
Now insert the above expression for $_n$ in
equation~(energy)Not in the term
$_n= e^{_n}/(1+ e^{_n})$.}.
The term proportional to $(1/2-h)/$ cancels the $ g$ term
of Eq.~(energy).
Averaging over the thermal fluctuations the resulting expression for
$$, we are
led to compute $_nS}/_{n'}$,
which can be written as

$$

_nS}}{_{n'}}
=-1}{Z}} [d] _n{_{n'}}
 e^{-S}}\, .

$$

Integrating by parts and taking into account that
$_n/_{n'}=_{nn'} _n (1-_n)$\, ,
we get

$$

_nS}}{_{n'}}
=_{nn'} _n (1-_n)\, .

$$

The term linear in $_n$ cancels the term proportional to
$^{-1}D}}^{-1}_{nn}$  of the averaged
Eq.~(energy). Hence, we obtain for the averaged energy

$$

=k_B T[3}{2}-1}{2}1}{V}_{nn'}
^{-1}_nD}}^{-1}_{nn'}_{n'}
+1}{2}1}{V}_{n}^{-1}
_nD}}^{-1}_{nn}_{n}]
\, .

$$

It suffices to write $n'=n+r$ to realize that the above equation is
Eq.~(avenergy).
thebibliography}{99}
peebles93}
 P.J.E. Peebles, *Principles of Physical Cosmology*
 (Princeton University Press, 1993).
einasto1}
U. Lindner, M. Einasto, J. Einasto, W. Freudling, K. Fricke,
V. Lipovetsky, S. Pustilnik, Y. Izotov, and G. Richter,
*Astron. Astrophys.* **314**, 1 (1996).
einasto2}
J. Einasto, astro-ph/0011334.
peebles01}
P.J.E. Peebles, *Ap. J.* **557**, 495 (2001).
pietronero}
F. Sylos Labini, M. Montuori, and L. Pietronero,
*Phys. Rep.* **293**, 61 (1998).
nonfractal:davis}
M. Davis, in *Critical Dialogues in Cosmology*,
Ed. N. Turok, (World Scientific, Singapore, 1997).
nonfractal:peebles}
P.J.E. Peebles, in
*Les Rencontrees de Physique de la Vallee d'Aosta*,
Ed. M. Greco (1998).
nonfractal:guzzo}
L. Guzzo, *New Astronomy* **2**, 517 (1997).
ism:larson}
R.B. Larson, *Mont. Not. R Astron. Soc.* **194**, 809 (1981).
ism:hetem}
A. Hetem jr. and J.R.D. Lepin, *Astron. Astrophys.* **270**,
451 (1993).
ism:kramer}
C. Kramer *et al.*
*Astron. Astrophys.* **329**, 249 (1998).
ism:stutzki}
J. Stutzki *et al.* *Astron. Astrophys.* **336**,
697 (1998).
dvsc}
H.J. De Vega, N. S\'anchez, and F. Combes, *Nature* **383**,
53 (1996);
*Phys. Rev.* **D54**, 6008 (1996).
pm}
T. Goldman, D. Hochberg, R. Laflamme, and J. P\'erez-Mercader,
*Phys. Lett.* **A222**, 177 (1996).
saslaw}
W. C. Saslaw, *Gravitational physics of stellar and galacti systems*
(Cambridge University Press, 1987).
coulomb:froelich}
J. Fr\"olich, in *Renormalization Theory*,
Eds. G. Velo and A.S. Wightman (Reidel, Dordrech/Boston, 1976).
coulomb:polyakov}
A.M. Polyakov, *Nucl. Phys.* **B20**, 429 (1977).
coulomb:samuel}
S. Samuel, *Phys. Rev.* **D18**, 1916 (1978).
pad}
T. Padmanabham, *Phys. Rep.* **188**, 285 (1990).
eduardo}
E. Follana and V. Laliena, *Phys. Rev.* **E61**, 6270 (2000).
gross}
D.H.E. Gross, *Microcanonical Thermodynamics* (World Scientific, 2001).
lynden-bell}
D. Lynden-Bell, in *Statistical Physics*,
Eds. A. Gervais, D. Iagolnitzer, M. Moreau, and Y. Pomeau
(North-Holland, 1999).
thirring}
P. Hertel and W. Thirring, *Ann. Phys. (N.Y.)* **63**, 520 (1971).
stahl}
B. Stahl, M.K.-H. Kiessling, and K. Schindler,
*Planet. Space Sci.* **43**, 271 (1995).
torcini}
A. Torcini and M. Antoni, *Phys. Rev.* **E59**, 2746 (1999).
chav:som}
P.-H. Chavanis and J. Sommeria,
*Mon. Not. R. Astr. Soc.* **296**, 569 (1998).
youngkins}
V.P. Youngkins and B.N. Miller, *Phys. Rev.* **E62**, 4583 (2000).
ispolatov}
I. Ispolatov and E.G.D. Cohen, *Phys. Rev.* **E64**, 056103 (2001).
chavanis}
P.-H. Chavanis, *Phys. Rev.* **E65**, 056123 (2002).
chav:isp}
P.-H. Chavanis and I. Ispolatov, *Phys. Rev.* **E66**,
036109 (2002).
devega}
H.J. De Vega and N. S\'anchez, *Phys. Lett.* **B490**, 180 (2000);
*Nucl. Phys.* **B625**, 409 (2002); *ibid* 460.
victor2}
V. Laliena, *Nucl. Phys.* **B668**, 403 (2003); astro-ph/0309225.
victor}
V. Laliena, *Phys. Rev.* **E59**, 4786 (1999).
emden}
R. Emden, *Gaskugeln* (Druck und Verlag von B.G. Teubner,
Leipzig, 1907).
chandra}
S. Chandrasekhar, *Stellar Structure* (Chicago University Press, 1939).
antonov}
V.A. Antonov, *Vest. leningr. gos. Univ.* **7**, 135 (1962).
wood}
D. Lynden-Bell and R. Wood, *Mon. Not. R. astr. Soc.* **138**,
 495 (1968).
gaite}
J. Gaite, A. Dom\'{nguez, and J. P\'erez-Mercader,
*Astrophys. J.* **522**, L5 (1999).
abdalla}
E. Abdalla and M. Rezha Rahimi Tabar, *Phys. Lett.* **B440**,
339 (1998).
thebibliography}
