#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#1,000,000th RedMart Customer Prize
import pandas as pd
from collections import deque
#
toteVol = 45 * 30 * 35                  #47250
cartVol,carts,highValuecart,minSeq = 0,[],[0],0
redMart = pd.read_csv('products.csv')
redMart.columns = ['proID','price','len','wid','hei','wt']
redMart['vol'] = redMart['len'] * redMart['wid'] * redMart['hei']
redMart = redMart[redMart.vol < 47251]
redMart = redMart.drop(['len','wid','hei'],axis=1)
#     redMart table columns - ProductId(0),Price(1),Weight(2),Volume(3)
volSort = redMart.sort_values(by=['vol'],ascending=True).values
priSort = redMart.sort_values(by=['price'],ascending=False).values
maxRange = len(volSort)
# add seq's total volume and compare with tote Volume
def calcVol(seq,volSort,carts,highValuecart,minSeq,cartVol,cartPri,cart):
#    print(seq)
#    input()
    brk = False
    if cartVol[0] > toteVol:
        remVal = seq[len(seq)-1]
        cartPrice = cartPri[0] - volSort[remVal][1]
        brk = True
    else:
        cartPrice = cartPri[0]
    if cartPrice > highValuecart[0]:
        Cart = list(cart)
        Cart.sort()
        print(f"${cartPrice} for {Cart}",flush=True)
        carts.clear()
        highValuecart[0] = cartPrice
        carts.append(Cart)
        for minSeq in range(maxRange):
            if cartPrice <= 0:
                minSeq -= 1
                break
            else:
                cartPrice -= priSort[minSeq][1]
    elif cartPrice == highValuecart[0]:
        Cart = list(cart)
        Cart.sort()
        print(f"${cartPrice} for {Cart}",flush=True)
        carts.append(Cart)
    return minSeq,brk
# t - pos in Seq,
def recur(t,seq,minSeq,cartVol,cartPri,cart):
#    print(seq)
    brk = False
    if t == len(seq)-1:
        while seq[t] < maxRange-1:
            if cartPri[0] >= highValuecart[0]:
                minSeq,brk = calcVol(seq,volSort,carts,highValuecart,minSeq,cartVol,cartPri,cart)
                if brk:
                    return minSeq,brk
#            print(cartVol,seq[t],volSort[seq[t]][3])
            if cartVol[0] <= toteVol:
                cart.pop()
                cartVol[0] -= volSort[seq[t]][3]
                cartPri[0] -= volSort[seq[t]][1]
                seq.append(seq.pop()+1)
                cartVol[0] += volSort[seq[t]][3]
                cartPri[0] += volSort[seq[t]][1]
                cart.append(volSort[seq[t]][0])
            else:
                return minSeq,brk
    else:
        minSeq,brk  = recur(t+1,seq,minSeq,cartVol,cartPri,cart)         
        if len(seq) < minSeq:
            return minSeq,brk
        while t != len(seq)-1:
            if seq[t] < maxRange-2:
                cart.pop()
                cart.pop()
                cartVol[0] = cartVol[0] - volSort[seq[t]][3] - volSort[seq[t+1]][3]
                cartPri[0] = cartPri[0] - volSort[seq[t]][1] - volSort[seq[t+1]][1]
                seq.pop()
                seq.append(seq.pop()+1)
                seq.append(seq[-1]+1)
                cart.append(volSort[seq[t]][0])
                cart.append(volSort[seq[t+1]][0])
                cartVol[0] += (volSort[seq[t]][3] + volSort[seq[t+1]][3])
                cartPri[0] += (volSort[seq[t]][1] + volSort[seq[t+1]][1])
                if cartVol[0] <= toteVol:
                    minSeq,brk = recur(t+1,seq,minSeq,cartVol,cartPri,cart)
                else:
                    if len(seq) >= minSeq:
                        cart.pop()
                        cartVol[0] -= volSort[seq[t+1]][3]
                        cartPri[0] -= volSort[seq[t+1]][1]
                        seq.pop()
                        while seq[t] < maxRange-1:
                            if cartPri[0] >= highValuecart[0]:
                                minSeq,brk = calcVol(seq,volSort,carts,highValuecart,minSeq,cartVol,cartPri,cart)
                                if brk:
                                    return minSeq,brk
                            if cartVol[0] <= toteVol:
                                cart.pop()
                                cartVol[0] -= volSort[seq[t]][3]
                                cartPri[0] -= volSort[seq[t]][1]
                                seq.append(seq.pop()+1)
                                cartVol[0] += volSort[seq[t]][3]
                                cartPri[0] += volSort[seq[t]][1]
                                cart.append(volSort[seq[t]][0])
                            else:
                                return minSeq,brk                            
                    return minSeq,brk                            
            else:
                for n in range(t+1,len(seq)):
                    cart.pop()
                    cartVol[0] -= volSort[seq[n]][3]
                    cartPri[0] -= volSort[seq[n]][1]
                    seq.pop()
                cart.pop()
                seq.append(seq.pop()+1)
                cart.append(volSort[seq[t]][0])
                if cartPri[0] >= highValuecart[0]:
                    minSeq,brk = calcVol(seq,volSort,carts,highValuecart,minSeq,cartVol,cartPri,cart)
                return minSeq,brk
        return minSeq,brk
#
for i in range(0,maxRange):
    cartVol,maxCombi = [0],0
#find max products require to fill toteVol
    for j in range(i,maxRange):
        cartVol[0] += volSort[j][3]
        maxCombi += 1
        if cartVol[0] > toteVol:
            maxCombi -= 1
            print(f"Max {maxCombi} products required to fill TOTE in Sequence: {i} and minimum Sequence is: {minSeq}")
            break
    if (i+maxCombi) < maxRange:
        maxSeq = maxCombi
    else:
        maxSeq = maxCombi - ((i+maxCombi) - maxRange)
    if maxSeq >= minSeq:
        seq = deque(range(i,i+maxSeq))
        cartVol, cartPri, cart = [0],[0],deque([])
        for n in range(len(seq)):
            cartVol[0] += volSort[seq[n]][3]
            cartPri[0] += volSort[seq[n]][1]
            cart.append(volSort[seq[n]][0])
        if cartPri[0] >= highValuecart[0]:
            minSeq,brk = calcVol(seq,volSort,carts,highValuecart,minSeq,cartVol,cartPri,cart)
#        print(seq,brk,minSeq)
        for j in range(maxSeq-1,0,-1):
            print("Iteration: {}, Minseq: {} ".format(j,minSeq))
            seq = deque(range(i,i+maxSeq))
            seq[j] += 1
            for k in range(j+1,maxSeq):
                if seq[k] < maxRange-2:
                    seq[k] = seq[k-1]+1
                else:
                    seq[k] = maxRange
                    seq = seq[:k+1]
            cartVol, cartPri, cart = [0],[0],deque([])
            for n in seq:
                cartVol[0] += volSort[n][3]
                cartPri[0] += volSort[n][1]
                cart.append(volSort[n][0])
#            input()
#            print("Start seq:",seq)
            minSeq,brk = recur(j,seq,minSeq,cartVol,cartPri,cart)
#            print("End   seq:",seq)
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
