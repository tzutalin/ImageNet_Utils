#!/usr/bin/env python
import scipy.io as sio
import numpy as np
import argparse

if '__main__' == __name__:
    p = argparse.ArgumentParser(description='Reorder meta data array.')
    p.add_argument('src', type=str, help='Input meta data')
    p.add_argument('idOrder', type=str, help='File listing the order of WNIDs')
    p.add_argument('dst', type=str, help='Output meta data')
    p.add_argument('--padding',dest='pad', action='store_true',
                   help='Pad empty item if WNID is not found')
    args = p.parse_args()

    KEY = 'synsets'
    src = sio.loadmat(args.src, squeeze_me=True)
    srcSynsets = src[KEY]

    dst = []
    with open(args.idOrder, 'rb') as order:
        for i, w in enumerate(order):
            w = w.strip()
            item = next((x for x in srcSynsets if w == x['WNID']), None)
            if item is None:
                if args.pad:
                    item = (w, '', '')
                else:
                    print('WNID = %s not found in %s!!' % (w, args.src))
                    exit()
            dst.append(tuple(item))

        # Check if the order is right
        order.seek(0, 0)
        for i, w in enumerate(order):
            if dst[i][0] != w.strip():
                print('Reordering fail!!')
                exit()
    dst = np.array(dst, dtype=srcSynsets.dtype)
    sio.savemat(args.dst, {KEY: dst})
