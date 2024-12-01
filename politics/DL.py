




def direct_lookahead(d_bar,alpha,beta,month):

    alpha = alpha[month - 1]
    beta = beta[month - 1]

    if d_bar == 0:
        return 600
    else :
        return d_bar + alpha*d_bar + beta*d_bar