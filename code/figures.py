import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.size': 9, 'font.family': 'sans-serif', 'axes.grid': False})

# ---------------------------------------------------------------- Assignment 1
def fig_prandtl():
    a=1.0; c=1.0; k=0.8
    y=np.linspace(-1.7,1.7,701); z=np.linspace(-1.05,1.05,701); Y,Z=np.meshgrid(y,z)
    phi=(1/(6*a))*(a-Z)*((Z+2*a)**2-3*Y**2-c**2)
    inside=(Z<=a)&(((Z+2*a)**2-3*Y**2)>=c**2)
    inner=(Z<=k*a)&(((Z/k+2*a)**2-3*(Y/k)**2)>=c**2)
    wall=inside&~inner
    phim=np.where(wall,phi,np.nan)
    fig,ax=plt.subplots(figsize=(6.2,4.2))
    levels=np.arange(0.015,0.226,0.015)
    cs=ax.contour(Y,Z,phim,levels=levels,cmap='coolwarm_r',linewidths=0.8)
    # boundaries
    zz=np.linspace(c-2*a,a,400); yy=np.sqrt(((zz+2*a)**2-c**2)/3)
    ax.plot(np.r_[yy,-yy[::-1]],np.r_[zz,zz[::-1]],'k',lw=1.2); ax.plot([-yy[-1],yy[-1]],[a,a],'k',lw=1.2)
    ax.plot(np.r_[k*yy,-k*yy[::-1]],np.r_[k*zz,k*zz[::-1]],'k',lw=1.0); ax.plot([-k*yy[-1],k*yy[-1]],[k*a,k*a],'k',lw=1.0)
    # annotations
    ax.plot(0,a,'o',color='red',ms=6); ax.annotate(r'max $|\tau_{xy}|$ (top centre)',(0,a),(0.15,1.12),color='red',arrowprops=dict(arrowstyle='->',color='red'),fontsize=8)
    for s in (-1,1):
        ax.plot(s*0.85,-0.22,'s',color='blue',ms=5)
    ax.annotate(r'max $|\tau_{xz}|$ (sides)',(0.85,-0.22),(0.62,-0.72),color='blue',arrowprops=dict(arrowstyle='->',color='blue'),fontsize=8)
    ax.annotate('',(-0.85,-0.22),(-0.6,-0.5),arrowprops=dict(arrowstyle='->',color='blue'))
    # inaccuracy regions: inner top corners
    for s in (-1,1):
        ax.add_patch(plt.Circle((s*k*yy[-1],k*a),0.17,fill=False,ls='--',color='purple',lw=1.4))
    ax.text(0,0.45,'highest inaccuracy:\ninner corners (dashed)',ha='center',color='purple',fontsize=8)
    ax.set_aspect('equal'); ax.set_xlabel('y / a'); ax.set_ylabel('z / a'); ax.set_xlim(-1.75,1.75); ax.set_ylim(-1.15,1.25)
    ax.set_title(r'Prandtl function $\phi/(G\theta^\prime a^2)$ of the solid section, plotted in the wall ($c=a$, $k=0.8$)',fontsize=8)
    fig.colorbar(cs,ax=ax,shrink=0.8,label=r'$\phi/(G\theta^\prime a^2)$')
    fig.tight_layout(); fig.savefig(f'{OUT}/a1_prandtl.pdf'); plt.close(fig)

def fig_eta():
    k=np.linspace(0,0.999,400)
    fig,ax=plt.subplots(figsize=(5.2,3.2))
    ax.plot(k,1+k**2,'b',label=r'$\eta(k)=(1-k^4)/(1-k^2)=1+k^2$')
    ax.plot(k,1-k**4,'r--',label=r'$I_{p,hollow}/I_{p,solid}=M_{t,hollow}/M_{t,solid}=1-k^4$')
    ax.plot(k,1-k**2,'g:',label=r'$A_{hollow}/A_{solid}=1-k^2$')
    ax.set_xlabel('scaling factor k'); ax.set_ylabel('ratio [-]'); ax.set_ylim(0,2.05); ax.grid(alpha=0.3); ax.legend(fontsize=7,loc='center left')
    fig.tight_layout(); fig.savefig(f'{OUT}/a1_eta.pdf'); plt.close(fig)

# ---------------------------------------------------------------- Assignment 2: B2 shear flow sketch
def arrow(ax,p1,p2,q,color='C3',scale=1.0,label=None,lw=None):
    p1=np.array(p1,float); p2=np.array(p2,float)
    if q<0: p1,p2=p2,p1; q=-q
    m=(p1+p2)/2; d=(p2-p1)/np.linalg.norm(p2-p1)
    L=min(0.4,np.linalg.norm(p2-p1)*0.45)
    ax.add_patch(FancyArrowPatch(m-d*L/2,m+d*L/2,arrowstyle='-|>',mutation_scale=7+120*q,color=color,lw=0.6+45*q,shrinkA=0,shrinkB=0))
    if label:
        n=np.array([-d[1],d[0]]); ax.text(*(m+n*0.2),label,fontsize=5.5,ha='center',va='center',color=color)

def fig_B2_flow():
    a=1.0
    # walls: (p1,p2,thickness label, q per Mt/a^2) right half; positive = direction p1->p2 for CCW cell flow
    q1,q2,q3,q4,q5 = 0.0331,0.0312,0.0278,0.0225,0.0203
    walls=[((0,0),(1,0),'3',q1),((1,0),(2.5,0),'3',q2),((2.5,0),(4,0),'2',q3),((4,0),(4,1),'2',q3),
           ((1,1),(0,1),'3',q1),((2.5,1),(1,1),'3',q2),((4,1),(2.5,1),'3',q3-q4),
           ((1,0),(1,1),'3',q2-q1),((2.5,0),(2.5,1),'1',q3-q2),
           ((2.5,3),(2.5,1),'1',q4),((4,1),(4,3),'2',q4),((4,3),(2.5,3),'1',q4-q5),
           ((2.5,5),(2.5,3),'1',q5),((4,3),(4,5),'2',q5),((4,5),(2.5,5),'3',q5),((0,0),(0,1),'4',0.0)]
    fig,ax=plt.subplots(figsize=(6.4,4.2))
    for p1,p2,t,q in walls:
        for s in (1,-1):
            P1=(s*p1[0],p1[1]); P2=(s*p2[0],p2[1])
            ax.plot([P1[0],P2[0]],[P1[1],P2[1]],'k',lw=0.6+0.5*float(t))
            if abs(q)>1e-4:
                if s==1: arrow(ax,P1,P2,q,scale=15,label='%.4f'%abs(q))
                else: arrow(ax,P2,P1,q,scale=15)   # mirrored cells: same sense (CCW)
    ax.text(0,0.5,'0',fontsize=6,ha='center')
    for i,(x,y) in enumerate([(0.5,0.5),(1.75,0.5),(3.25,0.5),(3.25,2),(3.25,4)]):
        ax.text(x,y,f'q{i+1}',ha='center',va='center',fontsize=8,color='C0',bbox=dict(boxstyle='circle',fc='w',ec='C0',lw=0.5))
    ax.add_patch(FancyArrowPatch((0.6,2.4),(-0.6,2.4),connectionstyle='arc3,rad=-0.9',arrowstyle='-|>',mutation_scale=10,color='k',lw=1)); ax.text(0,3.55,r'$M_t$',ha='center',fontsize=9)
    ax.set_aspect('equal'); ax.set_xlim(-4.4,4.4); ax.set_ylim(-0.4,5.6); ax.axis('off')
    ax.set_title(r'Design B2: net shear flow per wall in units $M_t/a^2$ (arrow thickness $\propto q$); numbers on the right half',fontsize=8)
    fig.tight_layout(); fig.savefig(f'{OUT}/a2_b2_flow.pdf'); plt.close(fig)

# ---------------------------------------------------------------- Assignment 2.5: omega, S_omega
def fig_omega():
    a=1.0; A=8*a; B=5*a; ts=3.5; tb=6.5; e=3*B**2*ts/(A*tb+6*B*ts)
    # s runs from top of left side (s=0) down, along bottom, up right side; total 2B+A
    s1=np.linspace(0,B,200); z1=B-s1; om1=(A/2)*(e-z1)                  # left side: omega = A/2 (e - z)
    s2=np.linspace(0,A,300); y2=-A/2+s2; om2=-e*y2                       # bottom
    s3=np.linspace(0,B,200); z3=s3; om3=(A/2)*(z3-e)                     # right side
    S1=(A*ts/2)*(e*(B-z1)-(B**2-z1**2)/2)
    S0=S1[-1]
    S2=S0-(e*tb/2)*(y2**2-A**2/4)
    S3=S1[::-1]
    s=np.r_[s1,B+s2,B+A+s3]; om=np.r_[om1,om2,om3]; S=np.r_[S1,S2,S3]
    fig,axs=plt.subplots(1,3,figsize=(9.5,3.3),gridspec_kw={'width_ratios':[1.2,1.2,1.4]})
    axs[0].plot(s,om,'b'); axs[0].axvline(B,color='gray',lw=0.5); axs[0].axvline(B+A,color='gray',lw=0.5); axs[0].axhline(0,color='k',lw=0.5)
    axs[0].set_xlabel('s / a  (from top of port side)'); axs[0].set_ylabel(r'$\omega$ / $a^2$'); axs[0].set_title(r'sectorial coordinate $\omega(s)$',fontsize=8)
    axs[0].annotate('%.2f'%om[0],(0,om[0]),fontsize=7); axs[0].annotate('%.2f'%om1[-1],(B,om1[-1]),fontsize=7); axs[0].annotate('%.2f'%om[-1],(s[-1],om[-1]),fontsize=7,ha='right')
    axs[1].plot(s,S,'r'); axs[1].axvline(B,color='gray',lw=0.5); axs[1].axvline(B+A,color='gray',lw=0.5); axs[1].axhline(0,color='k',lw=0.5)
    axs[1].set_xlabel('s / a'); axs[1].set_ylabel(r'$S_\omega$ / $(a^3 t_p)$'); axs[1].set_title(r'sectorial static moment $S_\omega(s)$',fontsize=8)
    axs[1].annotate('%.1f'%S1.min(),(e,S1.min()),fontsize=7); axs[1].annotate('%.1f'%S0,(B,S0),fontsize=7); axs[1].annotate('%.1f'%S2.max(),(B+A/2,S2.max()),fontsize=7,ha='center')
    # sketch on section
    ax=axs[2]; ax.plot([-A/2,-A/2,A/2,A/2],[B,0,0,B],'k',lw=1.5)
    sc=0.12; scS=0.02
    ax.plot(-A/2-om1*sc,z1,'b',lw=0.8); ax.plot(y2,-om2*sc,'b',lw=0.8); ax.plot(A/2+om3*sc,z3,'b',lw=0.8)
    ax.fill_betweenx(z1,-A/2,-A/2-om1*sc,color='b',alpha=0.15); ax.fill_between(y2,0,-om2*sc,color='b',alpha=0.15); ax.fill_betweenx(z3,A/2,A/2+om3*sc,color='b',alpha=0.15)
    ax.plot(-A/2-S1*scS,z1,'r',lw=0.8); ax.plot(y2,-S2*scS,'r',lw=0.8); ax.plot(A/2+S3*scS,z3,'r',lw=0.8)
    ax.plot(0,-e,'k+',ms=8); ax.text(0.1,-e-0.2,'shear centre S\n(e = %.2f a below bottom)'%e,fontsize=7)
    ax.plot([-A/2,A/2],[e,e],'k:',lw=0.5); ax.text(A/2+0.1,e,'z = e',fontsize=7)
    ax.set_aspect('equal'); ax.set_xlim(-6.2,7.2); ax.set_ylim(-2.8,6.2); ax.axis('off')
    ax.set_title(r'blue: $\omega$ (warping $u\propto\omega$), red: $S_\omega$ (shear $\propto S_\omega/t$)',fontsize=8)
    fig.tight_layout(); fig.savefig(f'{OUT}/a2_omega.pdf'); plt.close(fig)

# ---------------------------------------------------------------- Assignment 3: configs 1,2 flow sketch
def fig_cfg_flow():
    b=1.0
    fig,axs=plt.subplots(2,1,figsize=(7.5,5.6))
    # config 1
    ax=axs[0]; ax.plot([0,5,5,0,0],[-1,-1,1,1,-1],'k',lw=1.6)
    for x in np.linspace(5/6,25/6,5):
        ax.plot([x,x],[1,0.5],'k',lw=0.8); ax.plot([x-1/8,x+1/8],[0.5,0.5],'k',lw=1.6)
        ax.plot([x,x],[-1,-0.5],'k',lw=0.8); ax.plot([x-1/8,x+1/8],[-0.5,-0.5],'k',lw=1.6)
    q=0.05
    for p1,p2 in [((0,-1),(5,-1)),((5,-1),(5,1)),((5,1),(0,1)),((0,1),(0,-1))]:
        arrow(ax,p1,p2,q,scale=10)
    ax.text(2.5,0,'single cell,  $A=10b^2$,  $q=M_t/(20b^2)$ in all plates\nopen stiffeners: no shear flow (St. Venant only)',ha='center',fontsize=8)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Configuration 1',fontsize=9)
    # config 2
    ax=axs[1]; ax.plot([0,5,5,0,0],[-1,-1,1,1,-1],'k',lw=1.6)
    for x in np.linspace(5/6,25/6,5):
        ax.plot([x,x],[1,0.5],'k',lw=0.8); ax.plot([x-1/8,x+1/8],[0.5,0.5],'k',lw=1.6)
    qm,qt=0.0503,0.0430
    for xc in (5/6,15/6,25/6):
        bl,br=xc-5/12,xc+5/12; cl,cr=xc-1/6,xc+1/6
        ax.plot([bl,cl,cr,br],[-1,-0.75,-0.75,-1],'k',lw=0.8)
        ax.plot([xc,xc],[-0.75,-0.5],'k',lw=0.8); ax.plot([xc-1/8,xc+1/8],[-0.5,-0.5],'k',lw=0.8)
        arrow(ax,(bl,-1),(br,-1),qt,scale=10,color='C2')
        arrow(ax,(cl,-0.75),(bl,-1),qm-qt,scale=10,color='C1'); arrow(ax,(br,-1),(cr,-0.75),qm-qt,scale=10,color='C1'); arrow(ax,(cr,-0.75),(cl,-0.75),qm-qt,scale=10,color='C1')
    for p1,p2 in [((0,-1),(5/12,-1)),((5/6+5/12,-1),(15/6-5/12,-1)),((15/6+5/12,-1),(25/6-5/12,-1)),((25/6+5/12,-1),(5,-1)),((5,-1),(5,1)),((5,1),(0,1)),((0,1),(0,-1))]:
        arrow(ax,p1,p2,qm,scale=10)
    ax.text(2.5,0.1,r'main cell: $q_m=0.0503\,M_t/b^2$ (red); trapezoid base: $q_t=0.0430$ (green);'+'\n'+r'trapezoid legs/crown: $q_m-q_t=0.0074$ (orange)',ha='center',fontsize=8)
    ax.set_aspect('equal'); ax.axis('off'); ax.set_title('Configuration 2',fontsize=9)
    fig.tight_layout(); fig.savefig(f'{OUT}/a3_flow.pdf'); plt.close(fig)

# ---------------------------------------------------------------- Assignment 4: analytical distributions (normalised)
def fig_a4():
    a=1.0; A=8*a; B=5*a; ts=3.5; tb=6.5; e=3*B**2*ts/(A*tb+6*B*ts)
    fig,axs=plt.subplots(1,3,figsize=(9.5,3.0))
    # (a) through thickness free warping shear: tau = 2 G theta' n  (n = distance from mid-plane)
    n=np.linspace(-1,1,50)
    axs[0].plot(2*n*tb/2,n*tb/2,'b',label=r'bottom plate ($t_{bp}=6.5t_p$): $\tau_{xy}$')
    axs[0].plot(2*n*ts/2,n*ts/2,'r',label=r'side shell ($t_{sp}=3.5t_p$): $\tau_{xz}$')
    axs[0].axhline(0,color='k',lw=0.5); axs[0].axvline(0,color='k',lw=0.5)
    axs[0].set_xlabel(r'$\tau/(G\theta^\prime t_p)$'); axs[0].set_ylabel(r'through-thickness coordinate $n/t_p$'); axs[0].set_title('free warping (St. Venant) shear stress',fontsize=8); axs[0].legend(fontsize=6)
    # (b) sigma_xx(s) ~ omega(s) ; (d) tau(s) ~ S_omega/t
    s1=np.linspace(0,B,200); z1=B-s1; om1=(A/2)*(e-z1); s2=np.linspace(0,A,300); y2=-A/2+s2; om2=-e*y2; s3=np.linspace(0,B,200); om3=(A/2)*(s3-e)
    S1=(A*ts/2)*(e*(B-z1)-(B**2-z1**2)/2); S0=S1[-1]; S2=S0-(e*tb/2)*(y2**2-A**2/4); S3=S1[::-1]
    s=np.r_[s1,B+s2,B+A+s3]; om=np.r_[om1,om2,om3]
    axs[1].plot(s,om,'b'); axs[1].axhline(0,color='k',lw=0.5); axs[1].set_xlabel('s / a'); axs[1].set_ylabel(r'$\sigma_{xx}/(E\theta^{\prime\prime}a^2)=\omega/a^2$')
    axs[1].set_title(r'constrained warping normal stress $\sigma_{xx}(s)$ (and $u(s)\propto\omega$)',fontsize=8)
    taus=np.r_[S1/ts,S2/tb,S3/ts]
    axs[2].plot(s,-taus,'r'); axs[2].axhline(0,color='k',lw=0.5); axs[2].set_xlabel('s / a'); axs[2].set_ylabel(r'$\tau_{s}/(E\theta^{\prime\prime\prime}a^3)=-S_\omega/(t\,a^3 t_p)$')
    axs[2].set_title(r'constrained warping shear stress $\tau(s)=-E\theta^{\prime\prime\prime}S_\omega/t$',fontsize=8)
    for ax in axs[1:]:
        ax.axvline(B,color='gray',lw=0.5); ax.axvline(B+A,color='gray',lw=0.5)
    fig.tight_layout(); fig.savefig(f'{OUT}/a4_analytical.pdf'); plt.close(fig)

# ---------------------------------------------------------------- Assignment 5
def fig_a5():
    import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from torsion_ode import solve_ship
    for pair,name in ((('B1','B2'),'a5_B1B2'),(('BU','BUH'),'a5_BU_BUH')):
        fig,axs=plt.subplots(1,2,figsize=(9,3.2))
        for key,c in zip(pair,('C0','C3')):
            s=solve_ship(key)
            axs[0].plot(s['x'],np.degrees(s['th']),c,label=key); axs[1].plot(s['x'],s['thp']*1e3,c,label=key)
        for ax in axs:
            for xb in (20,40,60,80): ax.axvline(xb,color='gray',lw=0.5,ls=':')
            ax.set_xlabel('x [m] (0 = aft end)'); ax.legend(fontsize=8); ax.grid(alpha=0.3)
            for i,lab in enumerate(['A','B','B','B','C']): ax.text(10+20*i,ax.get_ylim()[1]*0.95,lab,ha='center',va='top',fontsize=8,color='gray')
        axs[0].set_ylabel(r'twist $\theta$ [deg]'); axs[0].set_title(r'rotation $\theta(x)$, $M_t$ = 100 MNm',fontsize=8)
        axs[1].set_ylabel(r"twist rate $\theta^\prime$ [mrad/m]"); axs[1].set_title(r"twist rate $\theta^\prime(x)$",fontsize=8)
        fig.tight_layout(); fig.savefig(f'{OUT}/{name}.pdf'); plt.close(fig)

fig_prandtl(); fig_eta(); fig_B2_flow(); fig_omega(); fig_cfg_flow(); fig_a4(); fig_a5()
print(sorted(os.listdir(OUT)))
