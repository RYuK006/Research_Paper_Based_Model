---
paper_id: "arxiv:chao-dyn/9807006"
title: "Universal statistics of wave functions in chaotic and disordered systems"
authors:
  - Bambi Hu
  - Baowen Li
  - Weng-ge Wang
year: 2000
doi: null
source: "arxiv"
parser_used: "arxiv_latex"
parsed_at: "2026-11-09T05:09:07.374428+00:00"
equation_count: 7
table_count: 0
---

# Universal statistics of wave functions in chaotic and disordered systems

## Abstract

We study a new statistics of wave functions in several chaotic and disordered systems: the random matrix model, band random matrix model, the Lipkin model, chaotic quantum billiard and the 1D tight-binding model. Both numerical and analytical results show that the distribution function of a generalized Riccati variable, defined as the ratio of components of eigenfunctions on basis states coupled by perturbation, is universal, and has the form of Lorentzian distribution.

## Document Content

{}{}{}

{
Universal statistics of wave functions in
chaotic and disordered systems
}

{
Bambi
Hu,1,2}
Baowen Li,1,3}To whom correspondence should
be addressed. E-mail:
bwli@phibm.hkbu.edu.hk}
and Wenge Wang1,4}
}

1}Department of Physics and  Centre for Nonlinear Studies, Hong
Kong Baptist University, Hong Kong, China \\
2} Department of Physics, University of Houston, Houston TX
77204-506, USA\\
3} Department of Physics, National University of Singapore, 119620
Singapore\\
4} Department of Physics, South-east University, Nanjing
210096, China
}
 }{ }

05}{45Mt}{Quantum chaos}
71}{23-k}{Electronic structure of disordered solids}
72}{15Rn}{Localization  effects}
}

abstract}
We study a new statistics of wave functions in
several chaotic  and  disordered
systems:  the random matrix model, band
random matrix model, the Lipkin
model, chaotic quantum billiard and the 1D tight-binding model. Both
numerical and analytical results show
that the distribution function of a
generalized Riccati variable, defined as
the ratio of components of eigenfunctions on basis states coupled by
perturbation, is universal, and has the form of Lorentzian distribution.
abstract}
Statistics of eigenfunctions in disordered and chaotic systems are of
great interest in many branches of physics such as condensed matter
physics, nuclear physics, chemical physics, and in particular, in the
new developing field of quantum
chaos[WVPRL,Haake,GVZ91]. However, although
eigenfunctions contain more information
than eigenenergies, much less has been studied compared with the
eigenenergies.
The mostly studied property is the statistics of wave function
amplitude $|({ r})|^2$ and two
point correlation function $ ({ r_1})({ r_2})$.
The former one has been found to be
the Porter-Thomas distribution for time-reversal invariant systems whose
classical counterpart is chaotic. This is
predicted by the Random Matrix Theory [PT,Berry77,Voros79], and
confirmed  numerically[Li,Num] and experimentally[Exp]. The
later one, which is proportional to $J_0(kd)$ ($J_0$ is the Bessel
function of the zeroth order, $k$ the wave vector and $d$ the distance
between
the two points), was proposed by Berry[Berry77] for a chaotic billiard
within an
assumption that the wave function is a superposition of plane waves with
random coefficients. The two point correlation function
has been extended to large separation by Hortikar and
Srednicki[Srednicki] recently. A beautiful review for the
correlations of
wave functions in disordered systems has been given recently by Mirlin
[Mirlin].
In this Letter, we would like study another interesting statistics, namely
the statistics of the Riccati variable of wave functions (see,
e.g., [Luck]).
The Riccati variable has been studied in one-dimensional disordered
system, where it is
related to the reflection coefficient of waves. As we shall see later,
the Riccati variable can be easily related to the two-point
correlation function, but it contains more information than the correlation
function. Furthermore,
the Riccati variable
gives information about local fluctuation properties of
wave functions, and the form of its distribution is related to
properties of the perturbation of the physical models.
To seek a general universality of this quantity among different
quantum systems, our study will be extended to a wide range of
random matrix model, disordered and chaotic systems
such as the Random Matrix Model (RMM)[Mehta],
Band Random Matrix Model
(BRMM)[FM94], the Lipkin model [Lipkin] with chaotic
behavior in the classical limit,
a chaotic quantum billiard model[Bunim] and
a 1D tight-binding model in the case of weak disorder[AnTh].
In order to study the chaotic systems,
the Riccati variable for the 1D tight-binding model is first extended
to a series types of Riccati variable,
namely, type I, type II and so on.
Then, the statistics for type I
Riccati variable is
found analytically to be of a Lorentzian form for the RMM. Based on
this fact, we conjecture  that the distribution function of the
Riccati variable of type I is universal for all chaotic and
disordered
systems. Our numerical results on several such models support the
conjecture.
Furthermore, the form of the distribution of the other types
of Riccati variable gives information
on properties of chaotic eigenfunctions which can not be supplied
by, e.g., the statistics of intensity of wave functions.
Let's first consider a general case in which the Hamiltonians
can be written in the form

$$

H= H_0 +  V ,

$$

where $ $ is a parameter for adjusting the strength
of the perturbation.
Eigenvectors of $H_0$ and $H$
will be denoted by $|i$ and $| $ in what follows,
respectively, i.e.,

$$

H_0 |i = E^0_i |i ,
H |  = E_{ } |  .

$$

Usually the perturbation $V$ can be written in the form of $V= _t V_t$
with $V_t=U_t+U_t^{ }$ and $U_t$ coupling a basis state
to one of the other basis states only.
In this Letter, we choose the strength of
$V_t$ comparable with each other.
The component of an eigenstate $| $ on a basis state
$|i$ will be denoted by
$C_{ i} (=  i| $).
For simplicity, we consider the case that
both $H$ and $H_0$ are time-reversal invariant only,
so that $C_{ i}$ are real.
In the 1D tight-binding model
the so-called Riccati variable
is defined as the ratio of components of eigenfunctions of
the nearest sites, where the off-diagonal
elements of the Hamiltonian are non-zero for the nearest sits only.
A natural extension of the concept to the general case of $H$ in
Eq.~(H) is to define the Riccati variable as
$p_{ , (i,j)}= C_{ i} / C_{ j}$ for $|i $
and $|j $ coupled by a $V_t$ ($ i|V_t|j  0$).
Note that the label $j$ is determined by the label $i$ due to
$V_t$.
The distribution of $p_{ , (i,j)}$
for all possible $i$ of an eigenfunction, or of eigenfunctions with
eigenenergies in some energy range,
will be denoted by $f_E(p)$ (the subscript $E$ will be omitted
for brevity in what follows).
Furthermore, the ratio $p_{ , (i,j)}$ for $|i $ and
$|j $ not coupled by $V$ is also of interest here. When
$ i|V|j =0$ but $ i|V^2|j  0$,
the ratio $p_{ , (i,j)}$ will be called type II
Riccati variable. The Riccati variable mentioned above
for $|i  $ and $|j $ coupled by $V$, is
type I.
For $|i  $ and $|j  $ satisfying
$ i|V^n|j  0$ but $ i|V^{n-1}|j = 0$,
the ratio $p_{ , (i,j)}$ will be called type $n$
Riccati variable. The distribution of type $n$
Riccati variable is also denoted by $f(p)$.
Expressing $C_{ i}C_{ j} $ as $p_{ ,
(i,j)} C^2_{ j} $, one can see that for chaotic eigenfunctions,
whose components and ratios of components can be regarded as statistically
independent, the average value of $p_{ ,(i,j)}$
is directly related to the two-point correlation function of a fixed
distance by the relation
$ p_{ ,(i,j)}   C^2_{ j} 
=  C_{ i}C_{ j}  $
where $ C^2_{ j}  =1/N$.
{ Random Matrix Model.} -- We start our discussion with the
RMM[Mehta]. Choosing $ =1 $ in Eq. (H) and taking the
matrix elements of $H_0$ and $V$ in the $H_0$ representation to be
real random numbers with Gaussian distribution
($ H^2_{ik} = 1$), one has the Gaussian orthogonal
ensemble (GOE). The joint distribution of two arbitrary components
 $C_i$ and $C_j$ for an arbitrary eigenfunction is
(subscript $ $ omitted for brevity)

$$
 P(C_i,C_j) =   ((N+1)/2)}{
 ((N-1)/2) } (1-C^2_i - C^2_j)^{(N-3)/2}
 
$$

(see ref. [Haake]).
Then, the distribution $f(p)$ can be readily obtained

$$

f_{GOE}(p) =
 dC_i dC_j  (p - C_i}{C_j})P(C_i ,C_j)
=  1/  }{p^2 +1},

$$

which is a Lorentzian
distribution centered at $p=0$. Notice that the ratio of
any two components of eigenfunctions of the GOE is a type I Riccati
variable.
It is then natural to conjecture that
the distribution of type I Riccati variable for
chaotic eigenfunctions also has a Lorentzian form.
As will be shown below  numerically
for other models, the distribution of
the Riccati variable of type I for chaotic eigenfunctions
is in fact of a more general Lorentzian form, denoted by $f_L(p)$
in order to be distinguished from $f_{GOE}(p)$,
which may center at $p  0$,

$$

f_L(p)= a/{(p-s)^2+ a^2},

$$

where $a=1-s^2}$ and $s = p $ which is proportional
to the value of
two point correlation function for a fixed $|i-j|$.  In fact, $f_L(p)$
can be obtained under a condition more general than the RMM.
Consider a distribution
$f(p)$ for $p$  and the distribution $F(q)$ for $q=1/p$.
If $F(q)$ has the same form as $f(p) $, i.e.,
$F(q)=f(q)$, and $1/f(p)$  can be expanded as a
Taylor series
$1/f(p) = d_0 + d_1p + d_2 p^2 +
, $
then $f(p)$ must has the form of $f_L(p)$.
This can be proved  easily
by making use of the relation between $F(q)$ and $f(p)$
required by $q=1/p$, i.e.,
$F(q)=f(1/q)/q^2.$
{ Lipkin Model.} -- The first dynamical model employed
in the Letter
is a three-orbital schematic shell
model, called the Lipkin
model, which is bounded and conservative.
In this model there are totally $ $ particles
distributed in three orbitals.
Both the quantum and the corresponding
classical dynamics of the model
have already been known (see, e.g., Refs. [MKZ88,WIC97]).
The Hamiltonian used in Ref. [WIC97] has the form
of Eq. (H) with

$$

H_0=_1 K_{11} + _2 K_{22},
 V=
_{t=1}^4 _t V_{t},

$$

where

$$

V_{1}= K_{10}K_{10}+K_{01}K_{01},\, V_{2}=
K_{20}K_{20}+K_{02}K_{02},\\
V_{3}= K_{21}K_{20} + K_{02}K_{12},\, V_{4}= K_{12}K_{10}+
K_{01}K_{21}.

$$

Here $_i$ and $_t$ are parameters given in
[WIC97], for which the system
is almost chaotic when $ =2$.
The operators $K_{00}, K_{11}$ and $K_{22}$ are
particle number operators
of the orbitals 0, 1 and 2, and
$K_{rs}$ for $r  s$  are particle raising
and lowering operators, respectively.
The eigenstates of $H_0$ are
$|mn = A(m,n) K^m_{10} K^n_{20} |00,$
where $A(m,n)$ is the normalization coefficient, $m$ and
$n$ are particle numbers of the orbitals 1 and 2,
respectively. The total particle number
is conserved, and as a result the particle number of
the orbital 0 is $ -m-n$. In our calculations
we take $ =40$ and the dimension of the Hilbert
space is $N=( +1)( +2)/2= 861$.
The basis states $|mn$ can also be labeled in energy
order as $|i$. In $|i$-representation, the Hamiltonian
matrix is banded [WIC97].
For convenience, we can put the two labels
together with $m_i$ and $n_i$
indicating particle numbers of the orbital 1 and 2, respectively.
Eq. (V14)
tells that the perturbation
couples only four kinds of basis states with
definite values of $ m=m_i-m_j$ and $ n
=n_i - n_j$, e.g.,
$ m=  2 , n=0$ for $V_1$.
That is, there are totally four kinds of
Riccati variable of type one.
When $ =2$, in the middle energy region the
nearest-level-spacing distribution of the Lipkin
model is close to the Wigner distribution and the underlying
classical dynamics is almost chaotic (except a
few quite small regular islands).
For this perturbation strength, it has been found that
the distributions of all the four kinds of Riccati variable
of type I are quite close to the distribution $f_L(p)$.
As an example, in Fig. 1(a)
we present the distribution $f(p)$ (dots, in the logarithm scale)
for $p=C_{ i}/C_{ j}$
with $|i$ and $|j$ coupled by $V_{1}$.
In order to have a good statistics
we have diagonalized
51 Hamiltonian matrices with $| -2|  0.025$
and then put data obtained for eigenfunctions of
$ =430 - 450$ together.
The solid line in Fig. 1(a)
is the best fitting curve of the Lorentzian
form $f_L(p)$. The central parts of the $f(p)$ and the
fitting curve are presented in the inset of Fig. 1(a)
in the ordinary scale.
We would like to mention
that the center of the distribution $f(p)$
in Fig. 1(a) is not at $p=0$.
On the other hand,
for  Riccati variable of type $n$ with
$n  2$ (also for $ =2$), it has been found that
the distribution $f(p)$ deviates from the Lorentzian form $f_L(p)$,
and the larger $n$  the
larger the deviation is. In Fig. 1(b) an example
is given for the distribution of
type V Riccati variable
with $m_i - m_j=  7$ and $n_i - n_j =0$,
where deviation of $f(p)$ (dots) from the Lorentzian fitting
curve (solid line) is quite obvious.
However, when the perturbation strength
$ $ is increased further,
the deviation from $f_L(p)$
will become smaller. In fact, for each type of Riccati variable,
so long as the value of $ $ is large enough, the distribution
function will become Lorentzian.
For example, when $ =6$ the form of $f(p)$ for
type II Riccati variable can be fitted
as well as the $f(p)$ in Fig. 1(a)
by the Lorentzian
distribution $f_L(p)$.
Finally, we would like to mention that
if the system is not chaotic
the distribution $f(p)$ for all types of Riccati variable
deviates from the Lorentzian
distribution $f_L(p)$. The deviation increases with decreasing
$ $. When $ $ approaches to zero, namely, the system
becomes near integrable, the distribution $f(p)$ will approach to a
$ $ function.
{ Band Random Matrix Model.} --
Since the difference
between the Lipkin model
and the RMM lies in
the band structure of the Hamiltonian matrix
of the Lipkin model in $H_0$ representation,
we have also studied the distribution $f(p)$ for
the Band Random Matrix Model (BRMM).
For this model we take $ =1$
in Eq. (H) and $H_{ik}$ being
 real random numbers with Gaussian distribution
($ H^2_{ik} = 1$) for $|i-k|  b$ and zero otherwise.
When $b>1$, despite of whether the eigenfunctions are localized or
extended,  numerically it has
been found that the distribution $f(p)$ for Riccati variable of type I
($|i-j|  b$) is very
close to $f_{GOE}(p)$ (due to the randomness of $H_{ik}$ the center of
$f(p)$ is at $p=0$);
while for the distribution of Riccati variable of type
$n$ with $n >1$,
deviation of the $f(p)$ from $f_{GOE}(p)$ has been found
which enlarges gradually as $n$ increases.
An example is given in
Fig. 1(c) for $i-j=  4b$, i.e. type IV in which the difference
between the distribution
$f(p)$ (dots) and the fitting curve of the
Lorentzian form  (solid line)
is quite clear.
When $ $ is increased, similar to the case of the Lipkin
model, $f(p)$ distributions for Riccati variable of type $n$ with
$n >1$ will also approach to the Lorentzian form of $f_{GOE}(p)$.
In order to compare with the result for the Lipkin model
that centers of $f(p)$ are not necessarily at $p=0$,
we have tried to add
a constant to all the non-zero off-diagonal elements
of the BRMM. Then, it has been found that
the peak of $f(p)$ could indeed be
shifted (see Fig. 1(d))
to $s( 0)$. The value of $s$ has been found numerically in a good
agreement with two-point correlation function.
{ Chaotic Quantum Billiard.} --
Chaotic quantum billiards have been
widely studied as a prototype of quantum chaos. We take the
Bunimovich stadium[Bunim] as an example. A chaotic odd-odd
wave function of a stadium
with radius $R=1$ and $a=1$ has been calculated by plane wave
decomposition method[Li]. The
wave function is shown in the inset of Fig. 2(a). For this wave function
the statistics of the intensity $||^2$ is a Porter-Thomas
distribution. The distribution $f(p)$ for $p=(x,y)/(x,y + 
y)$ with a fixed $ y$ larger than the de
Broglie wavelength is shown in the figure, which is found to
be a very good Lorentzian.  The best fit by Eq. (lorentz) gives
rise to $s= p=0.16$. As was pointed out before, $s$ is
related to the two point correlation function at a fixed $ y$.
According to Berry's conjecture[Berry77], $
(x,y)(x,y+ y) = J_0(k y)$, where ${ A}$
($=1+/4$) is the area of the billiard, and $k y=10$ here.
Thus, we have $ p = { A}J_0(k y)=0.18$.
This value is very close to the one obtained above.
{ 1D Tight Binding Model.} -- Finally, although  statistical
properties of spectra and distribution of components of eigenfunctions
for classically chaotic quantum systems
are quite different from those of the 1D tight binding
model (Anderson model) in the case of weak disorder,
it has been found that for the tight-binding model
the distribution of Riccati variable of type I
is also close to the Lorentzian form.
For this model we take $v_{ik}=  _{i,k+1}
+  _{i,k-1}$ and $E^0_i$ being random numbers
with flat distribution in the region $[-1/2,1/2]$.
An example is given in Fig. 2(b) for the
case of $ =1.0$.
The agreement between
the $f(p)$ distribution (dots)
and the fitting curve of the Lorentzian
form $f_L(p)$ (solid lines)
is quite obvious.
In conclusion,
for all different chaotic and disordered models studied in this Letter,
we have shown that
the distribution $f(p)$ for type I Riccati variable
is universal and has the
form of Lorentzian distribution.
On the other hand,  the distribution function for
Riccati variable of type $n$ with $n>1$,
although approaching to the Lorentzian form when
perturbation is strong enough,
shows different features in different stages of perturbation strength
even though the systems are already chaotic.
Therefore,
statistics of Riccati variables of different types
reflects statistical properties of eigenfunctions
that can not be reflected
by the statistics of wave function amplitude.
Furthermore, the properties of Riccati variable may supply
an alternative measure to probe
information for coupling structure (the Hamiltonian structure)
for real systems.

We are very grateful to G. Casati,  G.-S Tian and P.-Q
Tong for valuable discussions, J. M. Luck for introducing
us his interesting works on Riccati variables. We also thank the referees
for stimulating comments. This work was supported in parts by
the Hong Kong Research Grant Council (RGC), the Hong Kong
Baptist University Faculty Research Grant (FRG), Natural Science
Foundation of China, and the National Basic Research Project ``Nonlinear
Science'', China.
figure}
(a) The distribution function $f(p)$ (dots) of type I
Riccati variable
for the Lipkin model in chaotic region.
(b) Same as (a) but for type V. (c) The $f(p)$ of
type IV Riccati variable for the Band Random Matrix model, i.e. $i-j=20$
band width $b=5$. (d) The $f(p)$ (dots) obtained by
adding a constant to all the non-zero off-diagonal matrix
elements of BRMM. The solid curves in (a)-(d) are best
fitting curves of the Lorentzian form.  }

figure}
figure}
(a) The distribution function $f(p)$
(dots) of a chaotic eigenfunction
($k =E} = 200.119~670$) in stadium billiard.
The eigenfunction is shown in the
inset. (b) The $f(p)$ distribution  (dots)
of the 1D Anderson model in the case of weak
disorder.  The solid curves in (a) and (b) are  best fitting
curves of the  Lorentzian form.}
figure}
thebibliography}{99}
WVPRL}
Fyodorov  Y V, and Mirlin A D}
Phys. Rev. B}
51},
1995}
13403};
Prigodin V N}
Phys. Rev. Lett.}
74},
1995}
1566};
Prigodin V N, and Altshuler B L}
ibid}
80},
1998}
1944};
M\"uller K, Mehlig B, Milde F, and Schreiber M}
ibid}
78}
1997}
215};
Kaplann L}
ibid}
80}
1998}
2582}.
Haake}
Haake F}
Quantum Signatures of Chaos},
Springer-Verlag, Berlin,
1991}.
GVZ91}
Giannoni M J, Voros A, and Zinn-Justin J}(eds)
Chaos and Quantum Physics}, Elsevier, Amsterdam,
1991}.
PT}
Porter C E and Thomas R G}
Phys. Rev.}
104}
1956}
483};
Brody T A { et al}.}
Rev. Mod. Phys.}
53}
385}
1981}.
Berry77}
Berry M V}
J. Phys. A}
10}
1977}
2083}.
Voros79}
Voros A} in
Stochastic Behavior in Classical and
Quantum Hamiltonian Systems}
Eds. Casati G and Ford J.
Lecture Notes in Physics}
93}
1979}
326}.
Srednicki}
Hortikar S and Srednicki M}
Phys. Rev. Lett.}
80}
1646}
1998}.
Li}
Li B and Robnik M}
J. Phys. A}
27}
1994}
5509};
Borgonovi F, Casati G, and Li B}
Phys. Rev. Lett.}
77}
1996}
4744};
Li B}
Phys. Rev. E}
55}
1997}
5376};
Li B and Hu B}
J. Phys. A}
30}
483}
1998}.
Num}
Aurich R and Steiner F}
Physica D}
64}
1993}
185};
Exp}
Kudrolli A, Kidambi V, and Sridhar S}
Phys. Rev. Lett.}
75}
1995}
822}.
Mirlin}
Mirlin A D} in:
Supersymmetry and Trace Formulae: Chaos and
Disorder}
Eds.
Lerner I V, Keating J P and Khmelnitski D E}
Plenum, NY
1998},
245-260}.
Luck}
Barnes C and Luck L M}
J. Phys. A}
23}
1990}
1717};
Luck J M} in
Syst\'emes D\'esordonn\'es Unidimensioneels} 209},
Coolection Al\'ea Saclay, 1992}.
Mehta}
Mehta M L}
Random Matrices} Academic Press, San Diego, Second Edition,
1991};
Guhr T, M\"{u}ller-Groeling A, and
Weidenm\"{u}ller H A}
Phys. Rep.}
299}
1998}
189}.
FM94}
Fyodorov Y V and  Mirlin A D}
Int. J. Mod. Phys.}
8}
1994}
3795}; Izrailev F M}
Chaos, Solitons \& Fractals}
5}
1995}
1219}.
Lipkin}
Lipkin H J, Meshkov N, and Glick A J}
Nucl. Phys.}
62}
1965}
188}.
Bunim}
Bunimovich L A}
Commun. Math. Phys.}
65}
1979}
295}.
AnTh}
Anderson P W}
Phys. Rev. }
109}
1958}
1492};
Thouless D J}
Phys. Rep.}
13}
1974}
93}.
MKZ88}
Meredith D C, Koonin S E, and Zirnbauer M R}
Phys. Rev. A}
37}
1988}
3499};
Xu G O, Gong J B,
Wang W G, Yang Y T, and Fu D J}
Phys. Rev. E}
51}
1995}
1770}.
WIC97}
Wang W G, Izrailev F M, and Casati G}
Phys. Rev. E}
57}
1998}
323}.
thebibliography}
