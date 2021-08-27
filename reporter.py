#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module experiments with dataclasses and 
    creates a reporter for activities
"""

# standard libs
from dataclasses import dataclass

@dataclass
class StravaMap:
    _id: str
    resource_state: int
    summary_polyline: str

@dataclass(unsafe_hash=True)
class StravaActivity:
    id: int
    map: StravaMap

    def getSummaryPolyline(self) -> str:
        return self.map['summary_polyline']

'''
# Sample activity JSON
{'achievement_count': 10,
'athlete': {'id': 46800838, 'resource_state': 1},
'athlete_count': 1,
'average_speed': 2.979,
'comment_count': 0,
'commute': False,
'display_hide_heartrate_option': False,
'distance': 10100.1,
'elapsed_time': 3469,
'elev_high': 31.7,
'elev_low': 4.4,
'end_latlng': [-33.876673, 151.147573],
'external_id': '16c9a8a0-ff76-4590-b3c0-1969b6991643-activity.fit',
'flagged': False,
'from_accepted_tag': False,
'gear_id': None,
'has_heartrate': False,
'has_kudoed': False,
'heartrate_opt_out': False,
'id': 5859379159,
'kudos_count': 3,
'location_city': None,
'location_country': None,
'location_state': None,
'manual': False,
'map': {'id': 'a5859379159',
        'resource_state': 2,
        'summary_polyline': 'bmymEw|my[AMJW^a@PIBSCe@Qg@Ki@S]Ke@c@g@KQEBc@a@I[A_@KM{@e@U]_@U[i@aBgA]o@@KEOBGRM`@m@nAgAHm@EYISo@_AYi@YMe@DGOIe@CcCOgBGWOKGMBy@Mc@IEu@LcBK_@D]Wa@Ce@Ba@Ck@D]Jg@Ai@YS_@[_A[c@gBgAgBo@q@Ae@m@e@Sg@MUa@]WQIeAGYO_@I_AGa@N]GmDiBO[Oo@YSi@k@i@Y[[YK[A[a@_@YkD}A_AU_A?IQ@Op@uABICG}@Sk@_@k@C[Ok@g@MY_@_@O[q@a@WBYPINm@|D[nAKJo@`@OVs@x@_A`@}@j@[Za@t@Ef@OZOv@[rBStCY~AFnDFlAFj@T`BR`BbApC^xAm@fBiAjAw@^u@D}@EgAc@WSe@o@c@cAAcAMg@A]SaAY]GSU_CQw@iAeCU_ASa@Ws@M}@}@oDOc@SQk@S]A[T[Fi@VUj@SdAWl@m@hC]\\s@`@a@^s@XgAVs@Do@Ta@ESq@Q[MSo@a@Um@AyAGo@EuAD{@A}@Fw@?_BCiAu@gDGo@Oc@Wi@mAkA_@g@oBgB]k@u@s@Ui@w@sD[m@WW_@Qu@Ae@O]u@Ok@Sk@CWDs@pAgBf@sAF[@e@Ge@@s@C]LiAIe@a@g@UO_BVsA@w@J[EeAJQA_@QMMGQAWPq@EcA?sAV}@r@cB\\qAAiBLcA?}@D{@NOr@Sz@u@ZQ`@e@fBaBt@}@f@}@nA}At@}ARQj@gA\\eAZ_@R?JJFNAd@ML{@ZOb@@TTT\\Tx@PdAFb@RtBvBRf@Bv@F`@Zj@\\J~@BRPDLKd@C?ELAj@TzA`@xAL~@LTpAnAtAz@^j@Xv@Zl@F`AJh@hAxBb@pBt@rCVd@f@NLVDVC^GR[d@?d@n@nDh@|@b@bARRXHt@J`@NnA|@dA^VLTVLDn@Sd@DdABx@KrBHrAEbALlCt@TPVh@`@HPLb@|@l@X|@Fj@`@^`@VN\\HLXXPRDfAl@DJ?Fc@bADz@r@Yn@PfAx@r@PnAf@n@l@RLj@Nh@t@NFZ@t@z@'},
'max_speed': 5.2,
'moving_time': 3390,
'name': 'Lunch Run',
'photo_count': 0,
'pr_count': 1,
'private': False,
'resource_state': 2,
'start_date': '2021-08-27T01:19:27Z',
'start_date_local': '2021-08-27T11:19:27Z',
'start_latitude': -33.886412,
'start_latlng': [-33.886412, 151.136928],
'start_longitude': 151.147573,
'timezone': '(GMT+10:00) Australia/Sydney',
'total_elevation_gain': 33.7,
'total_photo_count': 0,
'trainer': False,
'type': 'Run',
'upload_id': 6230059842,
'upload_id_str': '6230059842',
'utc_offset': 36000.0,
'visibility': 'everyone',
'workout_type': 0}
'''