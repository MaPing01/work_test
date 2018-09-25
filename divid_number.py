def divid_nmuber( number ):
    int_number, float_number = divmod(round(number, 2), 1)
    f_number = round(float_number * 100)
    n_list = []
    for i in range(4, -1, -1):
        w = round(int_number) // (10 ** i)
        if w > 0:
            n_list.append(str(w * (10 ** i)))
            int_number -= w * (10 ** i)
        else:
            if i == 4 or i == 0:
                pass
            else:
                if len(n_list) > 0:
                    last = n_list[len(n_list) - 1]
                    if last != "0":
                        n_list.append("0")

    ln = len(n_list)
    rn_list = []

    if ln > 0:
        for j in range(ln - 1, -1, -1):
            if n_list[j] == '0' and j > 0:
                if n_list[j - 1] == '0':
                    rn_list.append(n_list[j])
        if len(rn_list) > 0:
            for rm in rn_list:
                n_list.remove(rm)

    n_list.append('point')
    for i in range(1, -1, -1):
        if f_number == 0:
            n_list.append("0")
        else:
            pw = round(f_number) // (10 ** i)
            n_list.append(str(pw))
            f_number -= pw * (10 ** i)
    return n_list

divid_nmuber(1005.55)