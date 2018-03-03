#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:17:16 2018

@author: oo
"""
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
maxRange = len(volSort)
#find max products require to fill toteVol
for maxCombi in range(maxRange):
    cartVol += volSort[maxCombi][3]
    if cartVol > toteVol:
        print(f"Max {maxCombi} products required to fill TOTE")
        break
# add seq's total volume and compare with tote Volume
def calcVol(seq,volSort,carts,highValuecart):
    cartVol = 0
    brk = False
    for i in range(len(seq)):
        cartVol += volSort[seq[i]][3]
        if cartVol > toteVol:
            brk = True
            break
        elif i == len(seq)-1:
            cartPri,cart = 0,[]
            for pri in seq:
                cartPri += volSort[pri][1]
                cart.append(volSort[pri][0])   #sequence of ProductID
            if cartPri > highValuecart[0]:
                cart.sort()
                print(f"${cartPri} for {cart}",flush=True)
                carts.clear()
                highValuecart[0] = cartPri
                carts.append(cart)                            
            elif cartPri == highValuecart[0]:
                cart.sort()
                for i in carts:
                    if i == cart:
                        break
                else:
                    print(f"${cartPri} for {cart}",flush=True)
                    carts.append(cart)
    return brk
#
for combi in range(maxCombi,0,-1):
    seq = list(range(combi))
    seq.sort(reverse=True)
    brk = calcVol(seq,volSort,carts,highValuecart)
    if not brk:
        for j in range(combi):
            for k in range(len(seq),maxRange):
                seq[j] = k
                seq.sort(reverse=True)
                brk = calcVol(seq,volSort,carts,highValuecart)
                if brk:
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