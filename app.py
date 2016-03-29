from flask import Flask, render_template, request, redirect

import os
import psycopg2
import urlparse

import numpy as np
from sklearn import linear_model as lm
from sklearn.metrics import r2_score
#import pandas as pd

from bokeh.plotting import *
from bokeh.embed import components
from bokeh.models import HoverTool,sources
from collections import OrderedDict

app = Flask(__name__)

geojsonFeature1='{"type": "Feature","properties": {"name": "some secsch","score":0.4}, "geometry" : {"type": "Polygon", "coordinates": [[[-73.73032599999999, 40.722156999999996], [-73.729652, 40.722535], [-73.729559, 40.72258], [-73.72914399999999, 40.722763], [-73.728734, 40.722913], [-73.728162, 40.723084], [-73.727972, 40.723158999999995], [-73.727328, 40.723411999999996], [-73.727217, 40.723456999999996], [-73.726838, 40.723608], [-73.72647599999999, 40.723752], [-73.726047, 40.723904999999995], [-73.725672, 40.724038], [-73.72508499999999, 40.724196], [-73.724722, 40.724314], [-73.724634, 40.724336], [-73.724547, 40.72436], [-73.724197, 40.724455], [-73.723868, 40.724544], [-73.723428, 40.724663], [-73.722912, 40.724793999999996], [-73.722579, 40.724878], [-73.722047, 40.725012], [-73.721733, 40.725105], [-73.721193, 40.725266999999995], [-73.721041, 40.725306], [-73.720913, 40.725339], [-73.72038599999999, 40.725474999999996], [-73.718288, 40.726044], [-73.716684, 40.726375], [-73.71585, 40.726478], [-73.71495999999999, 40.72659], [-73.714052, 40.726704999999995], [-73.71242099999999, 40.72691], [-73.7119, 40.726976], [-73.711308, 40.72705], [-73.71047, 40.727173], [-73.709954, 40.72728], [-73.70967, 40.727346], [-73.70943199999999, 40.727391], [-73.709081, 40.727464], [-73.708556, 40.727584], [-73.707647, 40.727796], [-73.707582, 40.72791], [-73.707129, 40.728702], [-73.70648, 40.729710999999995], [-73.705772, 40.73073], [-73.705269, 40.731513], [-73.704882, 40.731981], [-73.704869, 40.731997], [-73.704859, 40.732015], [-73.704599, 40.732502], [-73.70394499999999, 40.733526], [-73.70352199999999, 40.734207999999995], [-73.703315, 40.734563], [-73.70259000000001, 40.73551], [-73.702411, 40.735777999999996], [-73.70218899999999, 40.73611], [-73.702004, 40.73652200000001], [-73.701471, 40.737511999999995], [-73.70081100000002, 40.738439], [-73.700318, 40.738968], [-73.700204, 40.739070999999996], [-73.700107, 40.739159], [-73.70003799999999, 40.739221], [-73.70002, 40.739236999999996], [-73.700017, 40.739261], [-73.70001599999999, 40.739272], [-73.700009, 40.739323], [-73.70002, 40.73939], [-73.699879, 40.739473000000004], [-73.699744, 40.739557999999995], [-73.699009, 40.740027], [-73.698971, 40.740052], [-73.698942, 40.740069999999996], [-73.698346, 40.740449999999996], [-73.697529, 40.740959], [-73.696766, 40.741413], [-73.696052, 40.741833], [-73.695924, 40.741910999999995], [-73.695334, 40.74226], [-73.69462200000001, 40.742686], [-73.694341, 40.742866], [-73.69376799999999, 40.743198], [-73.693715, 40.743229], [-73.693139, 40.744921999999995], [-73.692979, 40.745445], [-73.692369, 40.746089], [-73.69259199999999, 40.747333], [-73.692045, 40.748612], [-73.691707, 40.749348], [-73.690797, 40.750143], [-73.690524, 40.750867], [-73.69083499999999, 40.751515000000005], [-73.690658, 40.752086], [-73.690448, 40.752876], [-73.68958099999999, 40.753654], [-73.689127, 40.754325], [-73.688996, 40.754652], [-73.688886, 40.754666], [-73.688684, 40.754688], [-73.68852, 40.754709999999996], [-73.68825199999999, 40.754737], [-73.687776, 40.754785999999996], [-73.687685, 40.754802], [-73.687085, 40.754902], [-73.686183, 40.754971], [-73.686143, 40.754974999999995], [-73.68585399999999, 40.754976], [-73.68525199999999, 40.754979999999996], [-73.68509499999999, 40.754979999999996], [-73.684105, 40.755001], [-73.682373, 40.755046], [-73.682113, 40.755043], [-73.68166599999999, 40.755006], [-73.68142, 40.75497], [-73.681175, 40.754925], [-73.680976, 40.754877], [-73.68073, 40.754748], [-73.68048499999999, 40.754701999999995], [-73.680032, 40.754673], [-73.678956, 40.75402700000001], [-73.67754800000002, 40.753177], [-73.676502, 40.752513], [-73.67621799999999, 40.752331], [-73.67456899999999, 40.751384], [-73.674448, 40.751307], [-73.673142, 40.750478], [-73.67280699999999, 40.750274999999995], [-73.67081999999999, 40.749067], [-73.670397, 40.748487999999995], [-73.670209, 40.748284], [-73.669921, 40.748025999999996], [-73.669232, 40.747478], [-73.669034, 40.747333], [-73.66801, 40.746614], [-73.66770799999999, 40.746405], [-73.666985, 40.745899], [-73.666783, 40.745747], [-73.666212, 40.745385999999996], [-73.666035, 40.74527500000001], [-73.664866, 40.744599], [-73.663466, 40.743789], [-73.66320700000001, 40.743648], [-73.662776, 40.743441], [-73.661975, 40.743057], [-73.66157199999999, 40.742894], [-73.661356, 40.742827], [-73.661125, 40.742771999999995], [-73.660344, 40.742646], [-73.659971, 40.742588999999995], [-73.659859, 40.742571999999996], [-73.65996200000001, 40.742515], [-73.65995, 40.742357999999996], [-73.659976, 40.742149999999995], [-73.660088, 40.741516], [-73.660264, 40.740533], [-73.66039099999999, 40.739782], [-73.660524, 40.739031], [-73.66065400000001, 40.738279], [-73.66078999999999, 40.737499], [-73.660926, 40.736717], [-73.661014, 40.736191999999996], [-73.660992, 40.736092000000006], [-73.660969, 40.735993], [-73.6609, 40.735707], [-73.66212, 40.735558999999995], [-73.663303, 40.735326], [-73.66375699999999, 40.73532], [-73.66467399999999, 40.735323], [-73.66592, 40.735043999999995], [-73.666794, 40.734876], [-73.667748, 40.734766], [-73.668683, 40.734635], [-73.66955899999999, 40.734466], [-73.670424, 40.734272000000004], [-73.671199, 40.734134999999995], [-73.671179, 40.733982], [-73.671038, 40.7334], [-73.671, 40.733286], [-73.67096699999999, 40.733185], [-73.670959, 40.733090999999995], [-73.672023, 40.732897], [-73.673152, 40.732631999999995], [-73.674893, 40.732226], [-73.676306, 40.731865], [-73.677774, 40.731504], [-73.67914499999999, 40.731168], [-73.679833, 40.731009], [-73.67945, 40.729667], [-73.67904899999999, 40.729714], [-73.67906099999999, 40.729403999999995], [-73.679071, 40.729192999999995], [-73.67966799999999, 40.729003], [-73.679558, 40.728421999999995], [-73.67948, 40.728009], [-73.67940899999999, 40.727641], [-73.679711, 40.72765], [-73.679761, 40.727359], [-73.68010199999999, 40.727267999999995], [-73.68052, 40.727269], [-73.680506, 40.727123000000006], [-73.68085099999999, 40.727194], [-73.680872, 40.726400999999996], [-73.681044, 40.726436], [-73.68156499999999, 40.726279999999996], [-73.681399, 40.725777], [-73.68135099999999, 40.725128999999995], [-73.68132899999999, 40.724833], [-73.68167799999999, 40.724834], [-73.68208, 40.724835], [-73.682164, 40.723143], [-73.682204, 40.723003999999996], [-73.682591, 40.721604], [-73.682692, 40.719328], [-73.682779, 40.71694000000001], [-73.682924, 40.716673], [-73.682476, 40.716634], [-73.681533, 40.716595000000005], [-73.67796299999999, 40.716555], [-73.67702899999999, 40.71653], [-73.676113, 40.716549], [-73.674165, 40.716555], [-73.673206, 40.716442], [-73.672336, 40.7166], [-73.671104, 40.716609], [-73.670462, 40.71758], [-73.66550200000002, 40.717518], [-73.664597, 40.717504], [-73.66411699999999, 40.717574], [-73.66369399999999, 40.717572], [-73.662792, 40.717569], [-73.66189299999999, 40.717566999999995], [-73.66099, 40.717555999999995], [-73.660994, 40.717400999999995], [-73.6601, 40.717349], [-73.6592, 40.71733100000001], [-73.65855599999999, 40.716771], [-73.65827399999999, 40.716901], [-73.658014, 40.716795999999995], [-73.657719, 40.716806999999996], [-73.656747, 40.716777], [-73.65281100000001, 40.717023], [-73.651625, 40.71695], [-73.651366, 40.716777], [-73.651197, 40.716645], [-73.65113199999999, 40.716554], [-73.651074, 40.7164], [-73.651314, 40.716317], [-73.65155299999999, 40.716232999999995], [-73.652372, 40.715967], [-73.652642, 40.715878], [-73.653229, 40.715683999999996], [-73.653526, 40.715579999999996], [-73.65413699999999, 40.715386], [-73.65478999999999, 40.715168999999996], [-73.655039, 40.715097], [-73.655226, 40.715030999999996], [-73.655414, 40.714966], [-73.65555499999999, 40.712385], [-73.65566799999999, 40.710398999999995], [-73.65567, 40.710369], [-73.655728, 40.710375], [-73.656553, 40.710473], [-73.657449, 40.710573], [-73.65745299999999, 40.710649], [-73.657631, 40.710397], [-73.657546, 40.710065], [-73.657264, 40.708802], [-73.655525, 40.707451999999996], [-73.656541, 40.706536], [-73.657324, 40.705829], [-73.657476, 40.705658], [-73.657623, 40.705677], [-73.657834, 40.704971], [-73.65802099999999, 40.704304], [-73.658239, 40.703602], [-73.658431, 40.702954999999996], [-73.658609, 40.702417], [-73.658643, 40.702279999999995], [-73.658996, 40.700876], [-73.659054, 40.700649], [-73.659112, 40.700368], [-73.659153, 40.700148999999996], [-73.65926, 40.700018], [-73.659666, 40.699518999999995], [-73.659767, 40.699363999999996], [-73.659883, 40.699127], [-73.65966, 40.697033], [-73.660048, 40.696948], [-73.66004099999999, 40.696428], [-73.660051, 40.695857], [-73.660096, 40.695671000000004], [-73.66014799999999, 40.695467], [-73.662885, 40.695499], [-73.66298499999999, 40.693448], [-73.664542, 40.692879], [-73.66554099999999, 40.692434999999996], [-73.666344, 40.692150999999996], [-73.666532, 40.692045], [-73.66662699999999, 40.691956999999995], [-73.66666699999999, 40.691894], [-73.667671, 40.691803], [-73.66766199999999, 40.691938], [-73.667609, 40.692288999999995], [-73.66759, 40.692344], [-73.667987, 40.692386], [-73.66821399999999, 40.692369], [-73.668363, 40.692296999999996], [-73.66865899999999, 40.692049999999995], [-73.668638, 40.692007], [-73.66864199999999, 40.691984999999995], [-73.66879, 40.691764], [-73.668672, 40.691489], [-73.669463, 40.691488], [-73.669636, 40.691466], [-73.67110799999999, 40.691361], [-73.67148399999999, 40.69132], [-73.67190099999999, 40.691311], [-73.672663, 40.690760999999995], [-73.67266599999999, 40.690681], [-73.67295800000001, 40.690608], [-73.673175, 40.690579], [-73.673506, 40.690571999999996], [-73.673867, 40.690594], [-73.67414099999999, 40.690642], [-73.674431, 40.690704], [-73.674363, 40.690843], [-73.67432699999999, 40.690964], [-73.67428, 40.691233], [-73.674871, 40.691182999999995], [-73.674936, 40.691176], [-73.675018, 40.691193999999996], [-73.683572, 40.693228], [-73.683664, 40.693064], [-73.684486, 40.693332], [-73.684702, 40.693402999999996], [-73.685067, 40.693522], [-73.685318, 40.693599], [-73.685538, 40.693667], [-73.685782, 40.69375], [-73.68583799999999, 40.69377], [-73.686139, 40.693872], [-73.686825, 40.694092], [-73.686882, 40.694114], [-73.68691799999999, 40.694144], [-73.686932, 40.694202], [-73.686927, 40.694212], [-73.686892, 40.694292], [-73.686522, 40.694952], [-73.686453, 40.695063000000005], [-73.686636, 40.695122999999995], [-73.687462, 40.695389], [-73.687918, 40.695175], [-73.689251, 40.694551], [-73.689792, 40.694297999999996], [-73.690214, 40.693964], [-73.691097, 40.693442999999995], [-73.69198399999999, 40.692921999999996], [-73.692363, 40.692721999999996], [-73.693202, 40.692277999999995], [-73.69396700000001, 40.691832999999995], [-73.694758, 40.691311999999996], [-73.69544100000002, 40.690889999999996], [-73.695854, 40.690871], [-73.696846, 40.690031999999995], [-73.697893, 40.689543], [-73.698577, 40.688946], [-73.699001, 40.688663], [-73.699185, 40.688556999999996], [-73.70017399999999, 40.688196999999995], [-73.7003, 40.687922], [-73.700362, 40.687812], [-73.70042, 40.687743000000005], [-73.700503, 40.687678], [-73.700693, 40.687591999999995], [-73.700875, 40.687506], [-73.70098700000001, 40.687418], [-73.70105199999999, 40.687339], [-73.701098, 40.687224], [-73.701751, 40.686665], [-73.702124, 40.68617], [-73.702229, 40.686146], [-73.70413599999999, 40.685724], [-73.704876, 40.685561], [-73.70610099999999, 40.683659999999996], [-73.7063, 40.683751], [-73.706814, 40.68397100000001], [-73.707116, 40.684101], [-73.707667, 40.683762], [-73.707848, 40.683659], [-73.708534, 40.683271], [-73.70936, 40.682956999999995], [-73.710436, 40.682666], [-73.71067599999999, 40.682379], [-73.710745, 40.682311], [-73.71111499999999, 40.682117999999996], [-73.71185, 40.681703], [-73.711979, 40.681551], [-73.712316, 40.681087999999995], [-73.712605, 40.679944000000006], [-73.712923, 40.679268], [-73.713257, 40.678619999999995], [-73.71402499999999, 40.678973], [-73.714062, 40.678920999999995], [-73.714124, 40.678808], [-73.714158, 40.678818], [-73.71488699999999, 40.677565], [-73.715649, 40.677953], [-73.717179, 40.678706999999996], [-73.717789, 40.679120999999995], [-73.718374, 40.679494], [-73.719066, 40.679764999999996], [-73.719291, 40.679863999999995], [-73.71944100000002, 40.679922], [-73.720034, 40.680254999999995], [-73.720762, 40.680661], [-73.72148899999999, 40.681067], [-73.72221499999999, 40.681472], [-73.722942, 40.681878], [-73.723669, 40.682283000000005], [-73.724395, 40.682688999999996], [-73.725121, 40.683093], [-73.725725, 40.683429], [-73.725843, 40.683575], [-73.725821, 40.683949999999996], [-73.725798, 40.684354], [-73.725878, 40.685514], [-73.725911, 40.686085], [-73.725918, 40.686099], [-73.725926, 40.68622500000001], [-73.72594099999999, 40.686399], [-73.725996, 40.686932], [-73.726089, 40.687774], [-73.72615800000001, 40.688469999999995], [-73.726175, 40.688649999999996], [-73.7262, 40.688984], [-73.72621699999999, 40.689305999999995], [-73.726231, 40.689659999999996], [-73.72623899999999, 40.689814999999996], [-73.726259, 40.690269], [-73.726258, 40.690611], [-73.726263, 40.69077300000001], [-73.726503, 40.696886], [-73.726509, 40.697522], [-73.726511, 40.697781], [-73.726525, 40.698257999999996], [-73.72654399999999, 40.698983], [-73.726654, 40.701111999999995], [-73.726713, 40.701448], [-73.726738, 40.701588], [-73.726783, 40.701986999999995], [-73.726751, 40.702079999999995], [-73.726728, 40.702146], [-73.72674599999999, 40.702473000000005], [-73.726762, 40.702768], [-73.726767, 40.702872], [-73.726772, 40.702954], [-73.726779, 40.703082], [-73.726781, 40.703145], [-73.726835, 40.704406], [-73.726871, 40.705237], [-73.72689500000001, 40.7058], [-73.727047, 40.709497], [-73.726896, 40.709976], [-73.7269, 40.709997], [-73.72697099999999, 40.710715], [-73.727086, 40.711259], [-73.727094, 40.711293], [-73.727165, 40.711588], [-73.727317, 40.712216], [-73.72733199999999, 40.712272], [-73.727364, 40.71239200000001], [-73.72751099999999, 40.712951], [-73.727698, 40.713662], [-73.728064, 40.715050999999995], [-73.728188, 40.715523999999995], [-73.728313, 40.715998], [-73.728418, 40.716391], [-73.728501, 40.716705999999995], [-73.728554, 40.71689800000001], [-73.72857599999999, 40.71698], [-73.72894, 40.718306], [-73.729176, 40.719167], [-73.729255, 40.719381], [-73.729433, 40.719865], [-73.729661, 40.720483], [-73.72969499999999, 40.720571], [-73.73032599999999, 40.722156999999996]]]}, "type": "Feature", "id": "0", "properties": {"INTPTLAT": "+40.7142717", "SDTYP": null, "SCSDLEA": "26520", "FUNCSTAT": "E", "INTPTLON": "-073.6937605", "LSAD": "00", "HIGRADE": "12", "AWATER": 205272.0, "LOGRADE": "07", "ALAND": 29838925.0, "MTFCC": "G5410", "GEOID": "3626520", "STATEFP": "36", "NAME": "Sewanhaka Central High School District"}}]}'

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['POST', 'GET'])
def index():

  if request.method == 'POST':

    # get user-defined search area (currently not used)
    query_center=request.form['center']
    query_radius=request.form['radius']
    query_features=request.form['features']
    feature_string = query_features
    
    # blah blah

    # get data from postgresql
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    try:
      #conn = psycopg2.connect("dbname='nysRealEstate' user='enghuiy' host='localhost' password=''")
      conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)

    except:
      return "Error: unable to connect to database"

    cur = conn.cursor()
    cur.execute("""SELECT refshape."NAME","ZPRICE","SCORE" from price2features JOIN refshape ON  price2features."refSHPindex"=refshape."refSHPindex" WHERE "SCORE" > 0;""")
    data=zip(*cur.fetchall())
    refnames = list(data[0])
    homevalue = list(data[1])
    features  = list(data[2])
    #print "%10f %4.1f" %(homevalue[0],features[0]) 

    # run linear regression

    coeffs,intercept,r2,ypredicted =  linearRegression(features,homevalue)
    
    ypredicted_scaled = [ x / 1 for x in ypredicted]
    homevalue_scaled = [ x / 1 for x in homevalue]

    # plot with bokeh
    #plot = figure(width=450, height=450, y_axis_label='Home Price', x_axis_label='Features')
    #plot.line(y,y,color='green',line_width=2)
    featureIndex=1
    script, div = plotLR(features,homevalue_scaled,ypredicted_scaled,refnames,coeffs[featureIndex],intercept,r2)

    return render_template('graph.html', script=script, div=div, features=feature_string)
    #return render_template('temp.html',data=homevalue[0])

  return render_template('index.html')

@app.route('/map')
def map_test():

  geojsonFeature2 = { "type": "Feature", 
                     "properties": { "name": "Scarsdale", },
                     "geometry": {
                       "type": "Point",
                       "coordinates": [-73.775, 42]
                       }
                     }

  
  return render_template('map_test.html', gjson=geojsonFeature1)

#===================================================
# normalization
def norm(x_in,x_norm):
    
    x_mu = np.mean(x_in)
    x_range = np.amax(x_in) - np.amin(x_in)
    x_norm [:] = [ ( x - x_mu ) / float (x_range) for x in x_in]
    return (x_mu, x_range)

# convert back to abs value
def unnorm(x_mu, x_range, x_norm):
    x_out=[]
    x_out [:] = [ x*x_range+x_mu for x in x_norm ]
    return x_out

# univariate regression
def linearRegression(features,homevalue):
    X_train = np.asarray(zip( np.ones(len(features)),features))

    # Create linear regression object
    regr = lm.LinearRegression()
    regr.fit(X_train, homevalue)
    coeffs = regr.coef_
    intercept = regr.intercept_

    # convert y back to abs value
    y_predicted_norm = regr.predict(X_train)
    y_predicted = regr.predict(X_train)

    r2=r2_score(homevalue, y_predicted)

    return (coeffs,intercept,r2,y_predicted)

def linearRegression_mynorm(features,homevalue):
    x_norm=[]; y_norm=[]
    (x_mu,x_range) = norm(features,x_norm)
    (y_mu, y_range) = norm(homevalue, y_norm)

    X_train = np.asarray(zip( np.ones(len(x_norm)),x_norm))

    # Create linear regression object
    regr = lm.LinearRegression()
    regr.fit(X_train, y_norm)
    coeffs = regr.coef_
    intercept = regr.intercept_

    # convert y back to abs value
    y_predicted_norm = regr.predict(X_train)
    y_predicted = unnorm(y_mu,y_range,y_predicted_norm)

    r2=r2_score(y_norm, y_predicted_norm)

    return (coeffs,intercept,r2,y_predicted)


# plot with bokeh
def mtext(p, x, y, text):
    p.text(x, y, text=[text],
           text_color="green", text_font_style='bold',text_align="left", text_font_size="14pt")

def plotLR(feature1D,homevalue,y_predicted,refnames,coefficient,intercept,r2):

  TOOLS = 'box_zoom,box_select,resize,reset,hover'
  
  plot = figure(width=600, height=450,y_axis_label='Home Price ($)', x_axis_label='Features',tools=TOOLS)
  plot.line(feature1D,y_predicted,color='green',line_width=3)

  source = ColumnDataSource(
    data=dict(
      x=feature1D,
      y=homevalue,
      label=refnames
      )
    )

  plot.circle('x', 'y', color='grey',size=5, alpha=0.5, source=source)

  hover =plot.select(dict(type=HoverTool))
  hover.tooltips = OrderedDict([
    ("Locale", "@label"),
    ("(feature,price)", "(@x, @y)"),
    ])

  mtext(plot, min(feature1D) + 1,max(homevalue)-100000, "y = %6.2f x + (%6.2f)" %(coefficient,intercept))
  mtext(plot, min(feature1D) + 1,max(homevalue)-250000, "R2 = %5.3f" %(r2))

  script, div = components(plot)

  return (script, div)

# RUN
if __name__ == '__main__':
  app.run(port=33507)
#  app.run(debug=True)
