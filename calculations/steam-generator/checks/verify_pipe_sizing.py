"""Independent SI check of the saved Hurmet pipe-sizing results."""
from pathlib import Path
import math,re,json,sys
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'Steam and feedwater pipe sizing - Hurmet.md'
s=path.read_text();expected={}
scales={'MW':1e6,'MPa':1e6,'kPa':1e3,'Pa':1,'K':1,'J/kg':1,'kg/m3':1,'Pa*s':1,'m/s':1,'m':1,'mm':.001,'':1}
def inp(name):
 m=re.search(r'¢` '+name+r' = ([0-9.eE+-]+)\s*([^`]*?) `',s)
 assert m,name
 unit=m[2].strip().strip("'")
 return float(m[1])*scales[unit]
def out(name,value,scale=1):expected[name]=value if isinstance(value,bool) else value/scale;return value
qgen=out('GeneratorDuty',inp('ReactorDuty')/inp('GeneratorCount'),1e6)
mass=out('BranchMass',qgen/(inp('SteamEnthalpy')-inp('WaterEnthalpy')))
mtot=out('HeaderMass',mass*inp('GeneratorCount'))
def speed(q,d):return 4*q/(math.pi*d*d)
def friction(q,d,rho,mu,rough):
 re=rho*speed(q,d)*d/mu
 if re<2300:return 64/re
 assert re>=4000
 # Independent bisection for the Colebrook inverse-square-root friction factor.
 lo,hi=1.,100.
 for _ in range(90):
  x=(lo+hi)/2
  residual=x+2*math.log10(rough/(3.7*d)+2.51*x/re)
  if residual>0:hi=x
  else:lo=x
 return 1/((lo+hi)/2)**2
def loss(q,d,rho,mu,L,K,rough):return (friction(q,d,rho,mu,rough)*L/d+K)*rho*speed(q,d)**2/2
def wall(d,p,stress,e,w,y,a,tol):
 alpha=p/(2*(stress*e*w+p*y))
 return (alpha*d+a)/(1-tol-2*alpha)
results={}
for tag,svc,seg in [('SB','Steam','Branch'),('SH','Steam','Header'),('WB','Water','Branch'),('WH','Water','Header')]:
 rho,mu=inp(svc+'Density'),inp(svc+'Viscosity')
 q=out(svc+seg+'Flow',(mass if seg=='Branch' else mtot)/rho)
 L,K,rough=inp(seg+'Length'),inp(seg+'K'),inp('Roughness')
 vmax,limit=inp(svc+'VelocityLimit'),inp(seg+'LossLimit')
 dv=out(tag+'VelocityBore',math.sqrt(4*q/(math.pi*vmax)),.001)
 lo,hi=.025,5.
 for _ in range(70):
  mid=(lo+hi)/2
  if loss(q,mid,rho,mu,L,K,rough)>limit:lo=mid
  else:hi=mid
 dp=out(tag+'LossBore',hi,.001)
 step=inp('BoreStep');d=out(tag+'Bore',math.ceil(max(dv,dp)/step)*step,.001)
 v=out(tag+'Velocity',speed(q,d));out(tag+'Reynolds',rho*v*d/mu)
 out(tag+'Friction',friction(q,d,rho,mu,rough));lp=out(tag+'Loss',loss(q,d,rho,mu,L,K,rough),1000)
 out(tag+'HydraulicOK',v<=vmax and lp<=limit)
 p,S,e,w,y=[inp(svc+k) for k in ['DesignPressure','Stress','E','W','Y']]
 a,tol=inp('Allowance'),inp('MillTolerance')
 tr=out(tag+'RequiredNominal',wall(d,p,S,e,w,y,a,tol),.001)
 t=out(tag+'Wall',math.ceil(tr/inp('WallStep'))*inp('WallStep'),.001)
 od=out(tag+'OD',d+2*t,.001)
 tm=out(tag+'RequiredMinimum',p*od/(2*(S*e*w+p*y))+a,.001)
 delivered=out(tag+'DeliveredMinimum',(1-tol)*t,.001)
 out(tag+'WallMargin',delivered-tm,.001)
 capacity=out(tag+'PressureCapacity',2*S*e*w*(delivered-a)/(od-2*y*(delivered-a)),1e6)
 out(tag+'PressureOK',delivered>=tm and capacity>=p)
 results[tag]={'bore_mm':d*1000,'nominal_wall_mm':t*1000,'bare_od_mm':od*1000,'velocity_m_s':v,'loss_kPa':lp/1000,'pressure_capacity_MPa':capacity/1e6}
for svc,tag in [('Steam','S'),('Water','W')]:out(svc+'PathLoss',expected[tag+'BLoss']+expected[tag+'HLoss'])
out('SteamLossFraction',expected['SteamPathLoss']*1000/inp('OperatingPressure'))
for S in [60,80,100]:out(f'SHWallAt{S}',wall(expected['SHBore']*.001,inp('SteamDesignPressure'),S*1e6,inp('SteamE'),inp('SteamW'),inp('SteamY'),inp('Allowance'),inp('MillTolerance')),.001)
out('SHWallAtOperating',wall(expected['SHBore']*.001,24e6,inp('SteamStress'),inp('SteamE'),inp('SteamW'),inp('SteamY'),inp('Allowance'),inp('MillTolerance')),.001)
out('OriginalSteamHeaderVelocity',speed(mtot/inp('SteamDensity'),.8))
out('OriginalWaterHeaderVelocity',speed(mtot/inp('WaterDensity'),.5))
for name,value in expected.items():
 m=re.search(r'¢\?\?` '+re.escape(name)+r' = (?:(?!`).)*?〔([^〕]+)〕',s,re.S)
 assert m,('Missing saved result',name)
 got=m[1].replace(',','').strip()
 if isinstance(value,bool):assert got==str(value).lower(),(name,got,value)
 else:assert math.isclose(float(got),value,rel_tol=6e-7,abs_tol=5e-8),(name,got,value)
print(json.dumps({'verified_results':len(expected),'sizes':results},indent=2))
