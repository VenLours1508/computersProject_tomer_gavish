import matplotlib.pyplot as pp
import numpy as bg


def fit_linear(filename):
    f = open(filename)
    d = f.readlines()
    d = org(d)
    bg = ""
    bgbg = []
    bgbg = check(d[0][0], d[0][1], d[0][2], d[0][3])
    if bgbg == None:
        return
    xl = bgbg[0];
    dxl = bgbg[1]; yl = bgbg[2]; dyl = bgbg[3];
    # xl = 'x values list', dxl = 'dx values list', yl = 'y values list', dyl = 'y values list'
    xa = d[1]
    ya = d[2]
    xa, ya = axis_names(xa, ya)
    a, b = calc(xl, yl, dyl, dxl)
    pp.clf()
    pp.plot(xl, yl, 'ro', color='blue', markersize='1.3')
    pp.plot([min(xl), max(xl)], [a*min(xl)+b, a*max(xl)+b], color='red')
    pp.xlabel(xa)
    pp.ylabel(ya)
    pp.errorbar(xl, yl, xerr=dxl, yerr=dyl, ecolor='blue', fmt='None')
    pp.savefig("linear_fig.SVG")
    f.close()
    return

# creates an object that contains all the data in an organized way
def org(data):
    xa = None
    ya = None
    m = []
    minn = 0; midd = 0; maxx = 0;
    ab = [[0, 0, 0], [0, 0, 0]]
    raw = []
    # raw data place holder
    bg1 = False
    bg2 = False
    for line in data:
        line.replace('\n', ' ')
        mod = line.strip().split(' ')
        # modified data
        if 'axis:' in mod and 'x' in mod:
            xa = (mod[2:])
        elif 'axis:' in mod and 'y' in mod:
            ya = (mod[2:])
        elif 'a' in mod:
            ab[0] = change(mod[1:])
            bg1 = True
        elif 'b' in mod:
            ab[1] = change(mod[1:])
            bg2 = True
        else:
            if len(mod) > 0:
                if mod[0] != '':
                    raw.append(mod)
    # # raw.remove([''])
    dl = []
    # data list
    t = []
    # temporary place holder for data
    low = None
    # lower cased info
    for l in raw:
        # l = 'list', i = 'item'
        t = []
        low = None
        for i in l:
            low = i.lower()
            t.append(low)
        try:
            t.remove('')
            dl.append(t)
        except:
            dl.append(t)
    nl = ['x', 'dx', 'y', 'dy'] # names of axis list
    fd = [] # final data formation
    t = []
    sl = [] # list of strings
    if dl[0][1] in nl and dl[0][0] in nl: # if the data is sorted in columns
        for n in nl: # n = 'name'
            t = []
            p = 999
            if n in dl[0]:
                p = dl[0].index(n) # place of n in dl
                for r in range(1, len(dl)):
                    try:
                        t.append(float(dl[r][p]))
                    except:
                        continue
            fd.append(t)
    else:# if the data is sorted in rows
        for n in nl:
            t = []
            sl = None
            for l in dl:
                t = []
                if l[0] == n:
                    for i in l[1:]:
                        t.append(float(i))
                    fd.append(t)
    ans = [fd, xa, ya]
    if bg1 and bg2:
        search_best_parameter(ans, ab)
    return ans


def check(xl, dxl, yl, dyl): # checking for errors in the data
    if len(xl) != len(dxl) or len(xl) != len(yl) or len(yl) != len(dyl):
        errorPrints(0)
        return
    else:
        for v in dxl:
            if v <= 0:
                errorPrints(1)
                return
        for v in dyl:
            if v <= 0:
                errorPrints(1)
                return
    bgbg = [xl, dxl, yl, dyl]
    return bgbg



def calc(xData, yData, dy, dx):
    x = xData
    y = yData
    chi_notred = 0  # chi not reduced
    b_1divdy2 = []  # inicial 1/dy^2
    dy2 = []  # dy squart
    # build a list 1/dy^2
    for num in dy:
        b_1divdy2.append(1 / num ** 2)
        dy2.append(num ** 2)
    one_divid_dy2 = sum(b_1divdy2)

    # build a list of x^2
    x2 = []  # x squart
    for num in x:
        x2.append(num ** 2)
    xy = []
    # build list of x*y
    for i in range(0, len(x)):
        xy.append(x[i] * y[i])
    x_up = 0
    y_up = 0
    xy_up = 0
    x2_up = 0
    dy2_up = 0
    for i in range(len(x)):  # calculates the sum of all the upper values in the avg
        x_up = x_up + x[i] * b_1divdy2[i]
        y_up = y_up + y[i] * b_1divdy2[i]
        xy_up = xy_up + xy[i] * b_1divdy2[i]
        x2_up = x2_up + x2[i] * b_1divdy2[i]
        dy2_up = dy2_up + dy2[i] * b_1divdy2[i]

    x_avg_fin = (x_up / one_divid_dy2)
    y_avg_fin = (y_up / one_divid_dy2)
    dy2_avg_fin = (dy2_up / one_divid_dy2)
    x2_avg_fin = (x2_up / one_divid_dy2)
    xy_avg_fin = (xy_up / one_divid_dy2)
    a = (xy_avg_fin - (x_avg_fin * y_avg_fin)) / (x2_avg_fin - (x_avg_fin ** 2))
    da = (dy2_avg_fin / (len(x)*(x2_avg_fin - (x_avg_fin**2)))) ** 0.5
    b = y_avg_fin - (a * x_avg_fin)
    db = ((dy2_avg_fin * x2_avg_fin) / (len(dy)*(x2_avg_fin - (x_avg_fin**2)))) ** 0.5
    chi2_notred = 0
    for i in range(len(x)):
        k = y[i] - (a * x[i] + b)
        z = (k / dy[i]) ** 2
        chi2_notred = chi2_notred + z
    x_red = (chi2_notred / (len(dy) - 2))
    ab = [[]]
    print("a=", a, "+-", da)
    print("b=", b, "+-", db)
    print("chi2=", chi2_notred)
    print("chi2_reduced=", x_red)
    return a, b


def errorPrints(num):
    if num == 0:
        print('Input file error: Data lists are not the same length')
    elif num == 1:
        print('Input file error: Not all uncertainties are positive')
    return


def axis_names(x_axis_list, y_axis_list):
    #change the axis lists to strings
    x_axis_before = ''
    for i in range(0, len(x_axis_list)):
        x_axis_before = x_axis_before + ' ' + x_axis_list[i]
    x_axis = x_axis_before.strip() #remove white spaces from the end
    y_axis_before = ''
    for i in range(0, len(y_axis_list)):
        y_axis_before = y_axis_before + " " + y_axis_list[i]
    y_axis = y_axis_before.strip()
    return(x_axis,y_axis)


from math import sqrt
def search_best_parameter(ans,ab):
    sum1=0
    for n in bg.arange(1, len(ans[0][0])):
        sum1 = sum1 + ((ans[0][2][n] - (ab[0][0] * ans[0][1][n] + ab[1][0] )) / (ans[0][3][n])) ** 2
    minchi = sum1
    finala=0
    finalb=0
    for a in bg.arange(ab[0][0], ab[0][1], abs(ab[0][2])):
        for b in bg.arange(ab[1][0] + 1, ab[1][1], abs(ab[1][2])):
            check=0
            sum = 0
            for n in bg.arange(0, len(ans[0][0])):
                sum = ((ans[0][2][n]-(a*ans[0][0][n]+b))/(ans[0][3][n]))**2
                check+=sum
            if (check<minchi):
                minchi=check
                finala=a
                finalb=b
    minchired=minchi/sqrt(len(ans[0][0]))
    print("a=", finala, "+-", abs(ab[0][2]))
    print("b=", finalb, "+-", abs(ab[1][2]))
    print("chi2=", minchi)
    print("chi2_reduced=", minchired)
    arr = [[], []]
    for a in bg.arange(ab[0][0], ab[0][1], abs(ab[0][2])):
        check = 0
        sum=0
        for n in bg.arange(0, len(ans[0][0])):
            sum = ((ans[0][2][n] - (a * ans[0][0][n] + finalb)) / (ans[0][3][n])) ** 2
            check += sum
        print(sum, a)
        arr[0].append(sum)
        arr[1].append(a)
    pp.clf()
    pp.plot(arr[1], arr[0], color='blue')
    pp.xlabel("A")
    pp.ylabel("Chi^2")
    pp.savefig("numeric_sampling’.SVG")


def change(mod):
    m = []
    b = []
    minn = mod[0]
    maxx = mod[0]
    for a in mod:
        if abs(float(a)) < abs(float(minn)):
            minn = a
        if float(a) > float(maxx):
            maxx = a
    b = [minn, maxx]
    for a in mod:
        if a not in b:
            m.append(float(a))
    m.append(float(maxx));m.append(float(minn));
    return m


fit_linear("InputExcemple")
