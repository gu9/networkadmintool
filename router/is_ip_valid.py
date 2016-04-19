def ipvalid(ipp):
    s1=ipp
    a=s1.split(".")
    l=len(a)
    for i in range(0,(len(a))):
        if l==4 and (1<=int(a[0])<=233) and int(a[0])!=127  and (int(a[0])!=169 or int(a[1]!=254) ) and (0<=int(a[1])<=255) and (0<=int(a[2])<=255) and (0<=int(a[3])<=255) :
            break;
        else:
            print "ip is invalid "
            return None
    return True
