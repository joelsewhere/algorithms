from scipy import stats

def pooled_var(a, b):
    # Instantiate a count variable
    # that represents the numerator
    # of the pooled variance
    count = 0
    # Loop over the values in sample a
    for a_val in a:
        # Subtract the mean of sample a
        # from the value
        difference = a_val - a.mean()
        # Square the difference
        squared_difference = difference**2
        # Add the squared difference to the 
        # count variable
        count += squared_difference
    # Loop over the values in sample b
    for b_val in b:
        # Subtract the mean of sample b
        # from the value
        difference = b_val - b.mean()
        # Square the difference
        squared_difference = difference**2
        # Add the squared difference to the 
        # count variable
        count += squared_difference
    
    # Calculate the denominator
    # by adding the length of both samples
    # and subtracting two
    denominator = len(a) + len(b)-2
    
    # return the count divided by the
    # denominator
    return count/denominator

def students_t_stat(a,b):
    # Subtract the mean of sample b
    # from sample a (a-b)
    mean_difference = a.mean() - b.mean()
    # Calculate the pooled variance
    # using the pooled_var function
    pooled_variance = pooled_var(a,b)
    # Calculate the denominator
    # by multiplying the pooled variance
    # by the sum of 1 over the length 
    # of both sample sizes
    denominator = (pooled_variance * (1/len(a) + 1/len(b))) ** .5
    # return the mean difference divided by the denominator
    return mean_difference/denominator

def ttest_ind(a,b):
    # Calculate the t statistic
    # using the students_t_stat function
    t = students_t_stat(a,b)
    # Create a variable called 
    # positive_t by passing t into
    # np.abs
    positive_t = np.abs(t)
    # Create a dof variable 
    # (stands for degrees of freedom)
    # that adds the length of both samples
    # and subtracts 2
    dof = len(a) + len(b) - 2
    # Create a data_below_t variable
    # that passes positive_t and dof
    # into the stats.t.cdf function
    data_below_t = stats.t.cdf(positive_t, dof)
    # Create a variable called data_above_t
    # that subtracts data_below_t from 1
    data_above_t = 1-data_below_t
    # Create the two sides pvalue by
    # multiplying data_above_t by 2
    p = data_above_t * 2
    # return t and p
    return t,p

def welch_variables(sample):
    # Calculate the mean of the sample
    bar = sample.mean()
    # Calculate the variance of the sample
    var = sample.var(ddof=1)
    # Calculate the size of the sample
    n = len(sample)
    # Calculate the degrees of freedom
    dof = n - 1
    
    # return all of the calculations
    return (bar, var, n, dof)

def welch_dof(a,b):
    # Calculate the required variables 
    # for both samples using the welch_variable function
    a_bar, a_var, a_n, a_dof = welch_variables(a)
    b_bar, b_var, b_n, b_dof = welch_variables(b)
    
    # Calculate the numerator for the degrees of freedom
    dof_numerator = (a_var/a_n + b_var/b_n)**2
    # Calculate the denominator for the degrees of freedom
    dof_denominator = (a_var**2/(a_n**2 * a_dof) + b_var**2/(b_n**2 * b_dof))
    # Divide the numerator by the denominator
    dof = dof_numerator/dof_denominator
    # return the degrees of freedom
    return dof

def welchs(a,b):
    # Calculate the required variables 
    # for both samples using the welch_variable function
    a_bar, a_var, a_n, a_dof = welch_variables(a)
    b_bar, b_var, b_n, b_dof = welch_variables(b)
    
    # Subtracts the mean of sample b from 
    # the mean of sample a
    t_numerator = a_bar - b_bar
    # Divide the variance of both samples
    # by the sample size for each sample
    # Add the divisions together
    # And calculate the square root
    t_denominator = np.sqrt(a_var/a_n + b_var/b_n)
    # Divide the numerator by the denominator
    t = t_numerator/t_denominator
    # Calculate the degrees of freedom with
    # the welch_dof function
    dof = welch_dof(a,b)
    # Create a variable called 
    # positive_t by passing t into
    # np.abs
    positive_t = np.abs(t)
    # Create a data_below_t variable
    # that passes positive_t and dof
    # into the stats.t.cdf function
    data_below_t = stats.t.cdf(positive_t, dof)
    # Create a variable called data_above_t
    # that subtracts data_below_t from 1
    data_above_t = 1-data_below_t
    # Create the two sides pvalue by
    # multiplying data_above_t by 2
    p = data_above_t * 2
    # return t and p
    return t,p