def ip_valid(ipp,maskk):
    s1=ipp
    a=s1.split(".")
    l=len(a)
    for i in range(0,(len(a))):
        if l==4 and (1<=int(a[0])<=233) and int(a[0])!=127  and (int(a[0])!=169 or int(a[1]!=254) ) and (0<=int(a[1])<=255) and (0<=int(a[2])<=255) and (0<=int(a[3])<=255) :
            break;
        else:
            print "ip is invalid "
            return None
    mask_list={255,254,252,248,240,224,192,128,0}
    mask_input=maskk
    m=mask_input.split(".")
    mask_len=len(m)
    while True:
        if(mask_len==4 and int(m[0])==255) and (int(m[1]) in mask_list and int(m[2]) in mask_list and int(m[3]) in mask_list )and (int(m[0])>=int(m[1])>=int(m[2])>=int(m[3])):
            break
        else:
            print "invalid mask "
            return None

    ip_append_list=[]
    for index in range(0,len(a)):
        binary_index=bin(int(a[index])).split("b")[1]
        if len(binary_index)==8:
            ip_append_list.append(binary_index)
        elif len(binary_index)<8:
            ip_append_list.append(binary_index.zfill(8))
    #print ip_append_list
    bin_ip_join="".join(ip_append_list)
    #print bin_ip_join

    mask_append_list=[]
    for index in range(0,len(m)):
        binary_index=bin(int(m[index])).split("b")[1]
        if len(binary_index)==8:
            mask_append_list.append(binary_index)
        elif len(binary_index)<8:
            mask_append_list.append(binary_index.zfill(8))
    #print mask_append_list
    mask_join="".join(mask_append_list)
   #print type(mask_join)

    zeros_count=mask_join.count("0")
    nos_of_one=32-zeros_count
    nos_host=abs(2**zeros_count-2)
    #print nos_host
    broadcast_address=[]
    network_address=[]
    network_address=bin_ip_join[:nos_of_one]+"0"*zeros_count
    #print len(network_address)
    octet_net=[]
    for index_octet in range(0,len(network_address),8):
        octet=network_address[index_octet:index_octet+8]
        octet_net.append(octet)
    #print octet_net
    decimal_net=[]
    for index in range(0,len(octet_net)):
        decimal_net.append(str(int(octet_net[index],2)))
    decimal_net_join=".".join(decimal_net)
    return  decimal_net_join+"/"+str(nos_of_one)
