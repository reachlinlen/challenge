#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#1,000,000th RedMart Customer Prize
import pandas as pd
#
toteVol = 45 * 30 * 35                  #47250
cartVol,carts,highValuecart = 0,[],[]
highValuecart.append(0)
redMart = pd.read_csv('products.csv')
redMart.columns = ['proID','price','len','wid','hei','wt']
redMart['vol'] = redMart['len'] * redMart['wid'] * redMart['hei']
redMart = redMart[redMart.vol < 47251]
redMart = redMart.drop(['len','wid','hei'],axis=1)
#     redMart table columns - ProductId(0),Price(1),Weight(2),Volume(3)
volSort = redMart.sort_values(by=['vol'],ascending=True).values
priSort = redMart.sort_values(by=['price'],ascending=False).values
maxRange = len(volSort)
minSeq = 0
# add seq's total volume and compare with tote Volume
def calcVol(seq,volSort,carts,highValuecart,minSeq):
    cartVol = 0
    cartPri,cart = 0,[]
    for i in range(len(seq)):
        cartVol += volSort[seq[i]][3]
        cartPri += volSort[seq[i]][1]
        cart.append(volSort[seq[i]][0])
        if cartVol > toteVol:
            cartPri -= volSort[seq[i]][1]
            cart.pop()
            if cartPri > highValuecart[0]:
                cart.sort()
                print(f"${cartPri} for {cart}",flush=True)
                carts.clear()
                highValuecart[0] = cartPri
                carts.append(cart)
                for minSeq in range(maxRange):
                    if cartPri <= 0:
                        break
                    else:
                        cartPri -= priSort[minSeq][1]
            elif cartPri == highValuecart[0]:
                cart.sort()
                for i in carts:
                    if i == cart:
                        break
                else:
                    print(f"${cartPri} for {cart}",flush=True)
                    carts.append(cart)
            break
        elif i == len(seq)-1 and cartPri >= highValuecart[0]:
            if cartPri > highValuecart[0]:
                cart.sort()
                print(f"${cartPri} for {cart}",flush=True)
                carts.clear()
                highValuecart[0] = cartPri
                carts.append(cart)
                for minSeq in range(maxRange):
                    if cartPri <= 0:
                        break
                    else:
                        cartPri -= priSort[minSeq][1]
            elif cartPri == highValuecart[0]:
                cart.sort()
                for i in carts:
                    if i == cart:
                        break
                else:
                    print(f"${cartPri} for {cart}",flush=True)
                    carts.append(cart)
    return minSeq
#
for i in range(0,maxRange):
    cartVol,maxCombi = 0,0
#find max products require to fill toteVol
    for j in range(i,maxRange):
        cartVol += volSort[j][3]
        maxCombi += 1
        if cartVol > toteVol:
            print(f"Max {maxCombi} products required to fill TOTE in Sequence: {i} and minimum Sequence is: {minSeq}")
            break
    if (i+maxCombi) < maxRange:
        maxSeq = maxCombi
    else:
        maxSeq = maxCombi - ((i+maxCombi) - maxRange)
    if maxSeq >= minSeq:
        seq = list(range(i,i+maxSeq))
        minSeq = calcVol(seq,volSort,carts,highValuecart,minSeq)
        for j in range(maxSeq-1,0,-1):
            if j >= minSeq:
                for k in range(i+maxSeq,maxRange):
                    seq[j] = k
                    t = j+1               #traverse
                    while t < len(seq):
                        if k != maxRange:
                            k += 1
                            seq[t] = k
                        else:
                            seq = seq[:t]
                            break
                        t += 1
                    if len(seq) >= minSeq:
                        minSeq = calcVol(seq,volSort,carts,highValuecart,minSeq)
                    else:
                        break
            else:
                break
    else:
        break
#
print("The result is:",carts,highValuecart)
toteWt = 0
#
for cart in carts:
    cartWt = 0
    for pro in cart:
        cartWt += redMart[redMart.proID == pro].values[0][2]
    if toteWt == 0:
        toteWt = cartWt
        print(f"{cart} weight is {toteWt} while sum is {sum(cart)}")
    elif toteWt > cartWt:
        toteWt = cartWt
        print(f"{cart} weight is {toteWt} while sum is {sum(cart)}")
