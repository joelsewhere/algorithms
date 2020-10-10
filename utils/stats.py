def mean(x):
    return sum(x)/len(x)

def sqrt(number):
    return number**.5

def variance(x, df=0):
    m = mean(x)
    return sum([(point - m)**2 for point in x])/len(x)-df

def std(x, df=0):
    m = mean(x)
    return sqrt(variance(x, df=df))


def standard_error(x, df=0):
    return std(x, df=df)/sqrt(len(x))


