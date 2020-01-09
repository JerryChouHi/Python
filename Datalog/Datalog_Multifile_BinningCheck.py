# encoding:utf-8
# @Time     : 2019/10/24
# @Author   : Jerry Chou
# @File     :
# @Function : 1、多文件分析  2、校验SoftBin对应HardBin是否正确

from csv import reader
from datetime import datetime
from os.path import join, basename, abspath, isdir
from os import getcwd, listdir
from sys import argv, path
from progressbar import *

path.append(abspath(join(getcwd(), '..')))
import Common

row_offset = 5
col_offset = 4

bin_definition = [[('PCLK_O/S', 5, 5),
                   ('HSYNC_O/S', 5, 5),
                   ('VSYNC_O/S', 5, 5),
                   ('D9_O/S', 5, 5),
                   ('D8_O/S', 5, 5),
                   
                   ('D7_O/S', 5, 5),
                   ('D6_O/S', 5, 5),
                   ('D5_O/S', 5, 5),
                   ('D4_O/S', 5, 5),
                   ('D3_O/S', 5, 5),
                   ('D2_O/S', 5, 5),
                   ('D1_O/S', 5, 5),
                   ('D0_O/S', 5, 5),
                   ('SCL_O/S', 5, 5),
                   ('SDA_O/S', 5, 5),
                   ('RSTB_O/S', 5, 5),
                   ('PWDN_O/S', 5, 5),
                   ('DVDD_O/S', 5, 5),
                   ('VRamp_O/S', 5, 5),
                   ('VH_O/S', 5, 5),
                   ('VN1_O/S', 5, 5),
                   ('EXCLK_O/S', 5, 5),
                   ('PCLK_Leakage/iiL', 6, 5),
                   ('HSYNC_Leakage/iiL', 6, 5),
                   ('VSYNC_Leakage/iiL', 6, 5),
                   ('D9_Leakage/iiL', 6, 5),
                   ('D8_Leakage/iiL', 6, 5),
                   ('D7_Leakage/iiL', 6, 5),
                   ('D6_Leakage/iiL', 6, 5),
                   ('D5_Leakage/iiL', 6, 5),
                   ('D4_Leakage/iiL', 6, 5),
                   ('D3_Leakage/iiL', 6, 5),
                   ('D2_Leakage/iiL', 6, 5),
                   ('D1_Leakage/iiL', 6, 5),
                   ('D0_Leakage/iiL', 6, 5),
                   ('SCL_Leakage/iiL', 6, 5),
                   ('SDA_Leakage/iiL', 6, 5),
                   ('RSTB_Leakage/iiL', 6, 5),
                   ('PWDN_Leakage/iiL', 6, 5),
                   ('EXCLK_Leakage/iiL', 6, 5),
                   ('PCLK_Leakage/iiH', 6, 5),
                   ('HSYNC_Leakage/iiH', 6, 5),
                   ('VSYNC_Leakage/iiH', 6, 5),
                   ('D9_Leakage/iiH', 6, 5),
                   ('D8_Leakage/iiH', 6, 5),
                   ('D7_Leakage/iiH', 6, 5),
                   ('D6_Leakage/iiH', 6, 5),
                   ('D5_Leakage/iiH', 6, 5),
                   ('D4_Leakage/iiH', 6, 5),
                   ('D3_Leakage/iiH', 6, 5),
                   ('D2_Leakage/iiH', 6, 5),
                   ('D1_Leakage/iiH', 6, 5),
                   ('D0_Leakage/iiH', 6, 5),
                   ('SCL_Leakage/iiH', 6, 5),
                   ('SDA_Leakage/iiH', 6, 5),
                   ('RSTB_Leakage/iiH', 6, 5),
                   ('PWDN_Leakage/iiH', 6, 5),
                   ('EXCLK_Leakage/iiH', 6, 5),
                   ('iic_test', 7, 5),
                   ('DVDD_voltage', 9, 5),
                   ('VH_voltage', 9, 5),
                   ('VN1_voltage', 9, 5),
                   ('Active_AVDD', 12, 5),
                   ('Active_DOVDD', 12, 5),
                   ('PWDN_AVDD', 8, 5),
                   ('PWDN_DOVDD', 8, 5),
                   ('PWDN_Total', 8, 5),
                   ('PLCK_Freq', 9, 5),
                   ('BLC_R', 7, 5),
                   ('BLC_Gr', 7, 5),
                   ('BLC_Gb', 7, 5),
                   ('BLC_B', 7, 5),
                   ('BK_ImageCapture', 98, 5),
                   ('BK_DeadRowExBPix_R', 15, 6),
                   ('BK_DeadRowExBPix_Gr', 15, 6),
                   ('BK_DeadRowExBPix_Gb', 15, 6),
                   ('BK_DeadRowExBPix_B', 15, 6),
                   ('BK_DeadColExBPix_R', 14, 6),
                   ('BK_DeadColExBPix_Gr', 14, 6),
                   ('BK_DeadColExBPix_Gb', 14, 6),
                   ('BK_DeadColExBPix_B', 14, 6),
                   ('BK_Mean_R', 13, 6),
                   ('BK_Mean_Gr', 13, 6),
                   ('BK_Mean_Gb', 13, 6),
                   ('BK_Mean_B', 13, 6),
                   ('BK_StdDEV_R', 13, 6),
                   ('BK_StdDEV_Gr', 13, 6),
                   ('BK_StdDEV_Gb', 13, 6),
                   ('BK_StdDEV_B', 13, 6),
                   ('LT_ImageCapture', 99, 5),
                   ('LT_DRow_R', 25, 4),
                   ('LT_DRow_Gr', 25, 4),
                   ('LT_DRow_Gb', 25, 4),
                   ('LT_DRow_B', 25, 4),
                   ('LT_DCol_R', 24, 4),
                   ('LT_DCol_Gr', 24, 4),
                   ('LT_DCol_Gb', 24, 4),
                   ('LT_DCol_B', 24, 4),
                   ('LT_DRow_Color', 25, 4),
                   ('LT_DCol_Color', 24, 4),
                   ('LT_Mean_R', 23, 4),
                   ('LT_Mean_Gr', 23, 4),
                   ('LT_Mean_Gb', 23, 4),
                   ('LT_Mean_B', 23, 4),
                   ('LT_StdDEV_R', 23, 4),
                   ('LT_StdDEV_Gr', 23, 4),
                   ('LT_StdDEV_Gb', 23, 4),
                   ('LT_StdDEV_B', 23, 4),
                   ('LT_RI_R', 23, 4),
                   ('LT_RI_Gr', 23, 4),
                   ('LT_RI_Gb', 23, 4),
                   ('LT_RI_B', 23, 4),
                   ('LT_Ratio_GrR', 23, 4),
                   ('LT_Ratio_GbR', 23, 4),
                   ('LT_Ratio_GrB', 23, 4),
                   ('LT_Ratio_GbB', 23, 4),
                   ('LT_Ratio_GbGr', 23, 4),
                   ('LT_LostBit', 23, 4),
                   ('LT_LostBitSNR_SumDIFF_R', 23, 4),
                   ('LT_LostBitSNR_SumDIFF_Gr', 23, 4),
                   ('LT_LostBitSNR_SumDIFF_Gb', 23, 4),
                   ('LT_LostBitSNR_SumDIFF_B', 23, 4),
                   ('LB_LT_ImageCapture', 99, 5),
                   ('LB_LT_Mean_R', 23, 4),
                   ('LB_LT_Mean_Gr', 23, 4),
                   ('LB_LT_Mean_Gb', 23, 4),
                   ('LB_LT_Mean_B', 23, 4),
                   ('LB_LT_LostBit', 23, 4),
                   ('LB_LT_LostBitSNR_SumDIFF_R', 23, 4),
                   ('LB_LT_LostBitSNR_SumDIFF_Gr', 23, 4),
                   ('LB_LT_LostBitSNR_SumDIFF_Gb', 23, 4),
                   ('LB_LT_LostBitSNR_SumDIFF_B', 23, 4),
                   ('FW_LT_ImageCapture', 99, 5),
                   ('FW_LT_DRow_R', 36, 4),
                   ('FW_LT_DRow_Gr', 36, 4),
                   ('FW_LT_DRow_Gb', 36, 4),
                   ('FW_LT_DRow_B', 36, 4),
                   ('FW_LT_DCol_R', 36, 4),
                   ('FW_LT_DCol_Gr', 36, 4),
                   ('FW_LT_DCol_Gb', 36, 4),
                   ('FW_LT_DCol_B', 36, 4),
                   ('FW_LT_DRow_Color', 36, 4),
                   ('FW_LT_DCol_Color', 36, 4),
                   ('FW_LT_Mean_R', 36, 4),
                   ('FW_LT_Mean_Gr', 36, 4),
                   ('FW_LT_Mean_Gb', 36, 4),
                   ('FW_LT_Mean_B', 36, 4),
                   ('FW_LT_StdDEV_R', 36, 4),
                   ('FW_LT_StdDEV_Gr', 36, 4),
                   ('FW_LT_StdDEV_Gb', 36, 4),
                   ('FW_LT_StdDEV_B', 36, 4),
                   ('FW_LT_RI_R', 36, 4),
                   ('FW_LT_RI_Gr', 36, 4),
                   ('FW_LT_RI_Gb', 36, 4),
                   ('FW_LT_RI_B', 36, 4),
                   ('FW_LT_Ratio_GrR', 36, 4),
                   ('FW_LT_Ratio_GbR', 36, 4),
                   ('FW_LT_Ratio_GrB', 36, 4),
                   ('FW_LT_Ratio_GbB', 36, 4),
                   ('FW_LT_Ratio_GbGr', 36, 4),
                   ('LT_CornerLine', 26, 8),  # 4
                   ('LT_ScratchLine', 26, 8),  # 4
                   ('LT_Blemish', 31, 8),  # 4
                   ('LT_LineStripe', 27, 8),  # 4
                   ('LT_Particle', 32, 8),  # 4
                   ('BK_Cluster2', 30, 4),
                   ('LT_Cluster2', 30, 4),
                   ('BK_Cluster1', 29, 4),
                   ('LT_Cluster1', 29, 4),
                   ('WP_Count', 35, 6),
                   ('BK_Cluster3GrGb', 39, 4),
                   ('LT_Cluster3GrGb', 40, 4),
                   ('BK_Cluster3SubtractGrGb', 33, 4),
                   ('LT_Cluster3SubtractGrGb', 34, 4),
                   ('LB_BK_DeadRowExBPix_R', 45, 2),
                   ('LB_BK_DeadRowExBPix_Gr', 45, 2),
                   ('LB_BK_DeadRowExBPix_Gb', 45, 2),
                   ('LB_BK_DeadRowExBPix_B', 45, 2),
                   ('LB_BK_DeadColExBPix_R', 44, 2),
                   ('LB_BK_DeadColExBPix_Gr', 44, 2),
                   ('LB_BK_DeadColExBPix_Gb', 44, 2),
                   ('LB_BK_DeadColExBPix_B', 44, 2),
                   ('SR_LT_ImageCapture', 96, 5),
                   ('SR_LT_DRow_R', 55, 2),
                   ('SR_LT_DRow_Gr', 55, 2),
                   ('SR_LT_DRow_Gb', 55, 2),
                   ('SR_LT_DRow_B', 55, 2),
                   ('SR_LT_DCol_R', 54, 2),
                   ('SR_LT_DCol_Gr', 54, 2),
                   ('SR_LT_DCol_Gb', 54, 2),
                   ('SR_LT_DCol_B', 54, 2),
                   ('SR_LT_DRow_Color', 55, 2),
                   ('SR_LT_DCol_Color', 54, 2),
                   ('SR_LT_Mean_R', 53, 2),
                   ('SR_LT_Mean_Gr', 53, 2),
                   ('SR_LT_Mean_Gb', 53, 2),
                   ('SR_LT_Mean_B', 53, 2),
                   ('SR_LT_StdDEV_R', 53, 2),
                   ('SR_LT_StdDEV_Gr', 53, 2),
                   ('SR_LT_StdDEV_Gb', 53, 2),
                   ('SR_LT_StdDEV_B', 53, 2),
                   ('SR_LT_RI_R', 53, 2),
                   ('SR_LT_RI_Gr', 53, 2),
                   ('SR_LT_RI_Gb', 53, 2),
                   ('SR_LT_RI_B', 53, 2),
                   ('SR_LT_Ratio_GrR', 53, 2),
                   ('SR_LT_Ratio_GbR', 53, 2),
                   ('SR_LT_Ratio_GrB', 53, 2),
                   ('SR_LT_Ratio_GbB', 53, 2),
                   ('SR_LT_Ratio_GbGr', 53, 2),
                   ('SR_LT_LostBit', 53, 2),
                   ('SR_BK_ImageCapture', 96, 5),
                   ('SR_BK_DeadRowExBPix_R', 42, 2),
                   ('SR_BK_DeadRowExBPix_Gr', 42, 2),
                   ('SR_BK_DeadRowExBPix_Gb', 42, 2),
                   ('SR_BK_DeadRowExBPix_B', 42, 2),
                   ('SR_BK_DeadColExBPix_R', 41, 2),
                   ('SR_BK_DeadColExBPix_Gr', 41, 2),
                   ('SR_BK_DeadColExBPix_Gb', 41, 2),
                   ('SR_BK_DeadColExBPix_B', 41, 2),
                   ('SR_BK_Mean_R', 43, 2),
                   ('SR_BK_Mean_Gr', 43, 2),
                   ('SR_BK_Mean_Gb', 43, 2),
                   ('SR_BK_Mean_B', 43, 2),
                   ('SR_BK_StdDEV_R', 43, 2),
                   ('SR_BK_StdDEV_Gr', 43, 2),
                   ('SR_BK_StdDEV_Gb', 43, 2),
                   ('SR_BK_StdDEV_B', 43, 2),
                   # ('Diffuser2_LT_ImageCapture', 99, 5),
                   # ('Diffuser2_LT_WeakLineRow_R', 72, 4),
                   # ('Diffuser2_LT_WeakLineRow_Gr', 72, 4),
                   # ('Diffuser2_LT_WeakLineRow_Gb', 72, 4),
                   # ('Diffuser2_LT_WeakLineRow_B', 72, 4),
                   # ('Diffuser2_LT_WeakLineCol_R', 71, 4),
                   # ('Diffuser2_LT_WeakLineCol_Gr', 71, 4),
                   # ('Diffuser2_LT_WeakLineCol_Gb', 71, 4),
                   # ('Diffuser2_LT_WeakLineCol_B', 71, 4),
                   ('Binning', 2, 1),
                   ('All Pass', 1, 1)
                   ], [('VSYNC_O/S', 5, 5),
                       ('HSYNC_O/S', 5, 5),
                       ('PCLK_O/S', 5, 5),
                       ('EXCLK_O/S', 5, 5),
                       ('RSTB_O/S', 5, 5),
                       ('PWDN_O/S', 5, 5),
                       ('SDA_O/S', 5, 5),
                       ('SCL_O/S', 5, 5),
                       ('D0_O/S', 5, 5),
                       ('D1_O/S', 5, 5),
                       ('D2_O/S', 5, 5),
                       ('D3_O/S', 5, 5),
                       ('D4_O/S', 5, 5),
                       ('D5_O/S', 5, 5),
                       ('D6_O/S', 5, 5),
                       ('D7_O/S', 5, 5),
                       ('D8_O/S', 5, 5),
                       ('D9_O/S', 5, 5),
                       ('MCP_O/S', 5, 5),
                       ('MCN_O/S', 5, 5),
                       ('MDP0_O/S', 5, 5),
                       ('MDN0_O/S', 5, 5),
                       ('MDP1_O/S', 5, 5),
                       ('MDN1_O/S', 5, 5),
                       ('AVDD_O/S', 5, 5),
                       ('DOVDD_O/S', 5, 5),
                       ('VRamp_O/S', 5, 5),
                       ('VH_O/S', 5, 5),
                       ('VN1_O/S', 5, 5),

                       ('VSYNC_Leakage/iiL', 6, 5),
                       ('HSYNC_Leakage/iiL', 6, 5),
                       ('PCLK_Leakage/iiL', 6, 5),
                       ('EXCLK_Leakage/iiL', 6, 5),
                       ('RSTB_Leakage/iiL', 6, 5),
                       ('PWDN_Leakage/iiL', 6, 5),
                       ('SDA_Leakage/iiL', 6, 5),
                       ('SCL_Leakage/iiL', 6, 5),
                       ('D0_Leakage/iiL', 6, 5),
                       ('D1_Leakage/iiL', 6, 5),
                       ('D2_Leakage/iiL', 6, 5),
                       ('D4_Leakage/iiL', 6, 5),
                       ('D5_Leakage/iiL', 6, 5),
                       ('D3_Leakage/iiL', 6, 5),
                       ('D6_Leakage/iiL', 6, 5),
                       ('D7_Leakage/iiL', 6, 5),
                       ('D8_Leakage/iiL', 6, 5),
                       ('D9_Leakage/iiL', 6, 5),
                       ('MCP_Leakage/iiL', 6, 5),
                       ('MCN_Leakage/iiL', 6, 5),
                       ('MDP0_Leakage/iiL', 6, 5),
                       ('MDN0_Leakage/iiL', 6, 5),
                       ('MDP1_Leakage/iiL', 6, 5),
                       ('MDN1_Leakage/iiL', 6, 5),

                       ('VSYNC_Leakage/iiH', 6, 5),
                       ('HSYNC_Leakage/iiH', 6, 5),
                       ('PCLK_Leakage/iiH', 6, 5),
                       ('EXCLK_Leakage/iiH', 6, 5),
                       ('RSTB_Leakage/iiH', 6, 5),
                       ('PWDN_Leakage/iiH', 6, 5),
                       ('SDA_Leakage/iiH', 6, 5),
                       ('SCL_Leakage/iiH', 6, 5),
                       ('D0_Leakage/iiH', 6, 5),
                       ('D1_Leakage/iiH', 6, 5),
                       ('D2_Leakage/iiH', 6, 5),
                       ('D4_Leakage/iiH', 6, 5),
                       ('D5_Leakage/iiH', 6, 5),
                       ('D3_Leakage/iiH', 6, 5),
                       ('D6_Leakage/iiH', 6, 5),
                       ('D7_Leakage/iiH', 6, 5),
                       ('D8_Leakage/iiH', 6, 5),
                       ('D9_Leakage/iiH', 6, 5),
                       ('MCP_Leakage/iiH', 6, 5),
                       ('MCN_Leakage/iiH', 6, 5),
                       ('MDP0_Leakage/iiH', 6, 5),
                       ('MDN0_Leakage/iiH', 6, 5),
                       ('MDP1_Leakage/iiH', 6, 5),
                       ('MDN1_Leakage/iiH', 6, 5),

                       ('iic_test', 7, 5),
                       ('DVDD_voltage', 9, 5),
                       ('VH_voltage', 9, 5),
                       ('VN1_voltage', 9, 5),
                       ('Active_AVDD', 12, 5),
                       ('Active_DOVDD', 12, 5),
                       ('PWDN_AVDD', 8, 5),
                       ('PWDN_DOVDD', 8, 5),
                       ('PWDN_Total', 8, 5),

                       ('BLC_R', 7, 5),
                       ('BLC_Gr', 7, 5),
                       ('BLC_Gb', 7, 5),
                       ('BLC_B', 7, 5),
                       ('DVP27M30F_BK_Cap', 98, 5),
                       ('BK_DeadRowExBPix_R', 15, 6),
                       ('BK_DeadRowExBPix_Gr', 15, 6),
                       ('BK_DeadRowExBPix_Gb', 15, 6),
                       ('BK_DeadRowExBPix_B', 15, 6),
                       ('BK_DeadColExBPix_R', 14, 6),
                       ('BK_DeadColExBPix_Gr', 14, 6),
                       ('BK_DeadColExBPix_Gb', 14, 6),
                       ('BK_DeadColExBPix_B', 14, 6),
                       ('BK_MixDCol_VfpnQty_R', 14, 6),
                       ('BK_MixDCol_VfpnQty_Gr', 14, 6),
                       ('BK_MixDCol_VfpnQty_Gb', 14, 6),
                       ('BK_MixDCol_VfpnQty_B', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue0_R', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue0_Gr', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue0_Gb', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue0_B', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue1_R', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue1_Gr', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue1_Gb', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue1_B', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue2_R', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue2_Gr', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue2_Gb', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue2_B', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue3_R', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue3_Gr', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue3_Gb', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue3_B', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue4_R', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue4_Gr', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue4_Gb', 14, 6),
                       ('BK_MixDCol_VFPN_MaxValue4_B', 14, 6),
                       ('BK_Mean_R', 13, 6),
                       ('BK_Mean_Gr', 13, 6),
                       ('BK_Mean_Gb', 13, 6),
                       ('BK_Mean_B', 13, 6),
                       ('BK_StdDEV_R', 13, 6),
                       ('BK_StdDEV_Gr', 13, 6),
                       ('BK_StdDEV_Gb', 13, 6),
                       ('BK_StdDEV_B', 13, 6),

                       ('DVP27M30F_LT_Cap', 99, 5),
                       ('PLCK_Freq', 93, 5),
                       ('LT_DRow_R', 25, 4),
                       ('LT_DRow_Gr', 25, 4),
                       ('LT_DRow_Gb', 25, 4),
                       ('LT_DRow_B', 25, 4),
                       ('LT_DCol_R', 24, 4),
                       ('LT_DCol_Gr', 24, 4),
                       ('LT_DCol_Gb', 24, 4),
                       ('LT_DCol_B', 24, 4),
                       ('LT_DRow_Color', 25, 4),
                       ('LT_DCol_Color', 24, 4),
                       ('LT_WeakLineRow_R', 25, 4),
                       ('LT_WeakLineRow_Gr', 25, 4),
                       ('LT_WeakLineRow_Gb', 25, 4),
                       ('LT_WeakLineRow_B', 25, 4),
                       ('LT_WeakLineCol_R', 24, 4),
                       ('LT_WeakLineCol_Gr', 24, 4),
                       ('LT_WeakLineCol_Gb', 24, 4),
                       ('LT_WeakLineCol_B', 24, 4),
                       ('LT_Mean_R', 23, 4),
                       ('LT_Mean_Gr', 23, 4),
                       ('LT_Mean_Gb', 23, 4),
                       ('LT_Mean_B', 23, 4),
                       ('LT_StdDEV_R', 23, 4),
                       ('LT_StdDEV_Gr', 23, 4),
                       ('LT_StdDEV_Gb', 23, 4),
                       ('LT_StdDEV_B', 23, 4),
                       ('LT_RI_R', 23, 4),
                       ('LT_RI_Gr', 23, 4),
                       ('LT_RI_Gb', 23, 4),
                       ('LT_RI_B', 23, 4),
                       ('LT_Ratio_GrR', 23, 4),
                       ('LT_Ratio_GbR', 23, 4),
                       ('LT_Ratio_GrB', 23, 4),
                       ('LT_Ratio_GbB', 23, 4),
                       ('LT_Ratio_GbGr', 23, 4),
                       ('LT_LostBit', 23, 4),
                       ('LT_LostBitSNR_SumDIFF_R', 23, 4),
                       ('LT_LostBitSNR_SumDIFF_Gr', 23, 4),
                       ('LT_LostBitSNR_SumDIFF_Gb', 23, 4),
                       ('LT_LostBitSNR_SumDIFF_B', 23, 4),

                       ('DVP27M30F_LBIT_Cap', 99, 5),
                       ('LBIT_LT_Mean_R', 23, 4),
                       ('LBIT_LT_Mean_Gr', 23, 4),
                       ('LBIT_LT_Mean_Gb', 23, 4),
                       ('LBIT_LT_Mean_B', 23, 4),
                       ('LBIT_LT_LostBit', 23, 4),
                       ('LBIT_LT_LostBitSNR_SumDIFF_R', 23, 4),
                       ('LBIT_LT_LostBitSNR_SumDIFF_Gr', 23, 4),
                       ('LBIT_LT_LostBitSNR_SumDIFF_Gb', 23, 4),
                       ('LBIT_LT_LostBitSNR_SumDIFF_B', 23, 4),

                       ('DVP27M30F_FW_Cap', 99, 5),
                       ('FW_LT_DRow_R', 36, 4),
                       ('FW_LT_DRow_Gr', 36, 4),
                       ('FW_LT_DRow_Gb', 36, 4),
                       ('FW_LT_DRow_B', 36, 4),
                       ('FW_LT_DCol_R', 36, 4),
                       ('FW_LT_DCol_Gr', 36, 4),
                       ('FW_LT_DCol_Gb', 36, 4),
                       ('FW_LT_DCol_B', 36, 4),
                       ('FW_LT_DRow_Color', 36, 4),
                       ('FW_LT_DCol_Color', 36, 4),
                       ('FW_LT_Mean_R', 36, 4),
                       ('FW_LT_Mean_Gr', 36, 4),
                       ('FW_LT_Mean_Gb', 36, 4),
                       ('FW_LT_Mean_B', 36, 4),
                       ('FW_LT_StdDEV_R', 36, 4),
                       ('FW_LT_StdDEV_Gr', 36, 4),
                       ('FW_LT_StdDEV_Gb', 36, 4),
                       ('FW_LT_StdDEV_B', 36, 4),
                       ('FW_LT_RI_R', 36, 4),
                       ('FW_LT_RI_Gr', 36, 4),
                       ('FW_LT_RI_Gb', 36, 4),
                       ('FW_LT_RI_B', 36, 4),
                       ('FW_LT_Ratio_GrR', 36, 4),
                       ('FW_LT_Ratio_GbR', 36, 4),
                       ('FW_LT_Ratio_GrB', 36, 4),
                       ('FW_LT_Ratio_GbB', 36, 4),
                       ('FW_LT_Ratio_GbGr', 36, 4),
                       ('FW_LT_LostBit', 36, 4),

                       ('DVP27M30F_BSun_Cap', 96, 5),
                       ('BSun_BK_DeadRowExBPix_R', 48, 6),
                       ('BSun_BK_DeadRowExBPix_Gr', 48, 6),
                       ('BSun_BK_DeadRowExBPix_Gb', 48, 6),
                       ('BSun_BK_DeadRowExBPix_B', 48, 6),
                       ('BSun_BK_DeadColExBPix_R', 47, 6),
                       ('BSun_BK_DeadColExBPix_Gr', 47, 6),
                       ('BSun_BK_DeadColExBPix_Gb', 47, 6),
                       ('BSun_BK_DeadColExBPix_B', 47, 6),
                       ('BSun_BK_Mean_R', 46, 6),
                       ('BSun_BK_Mean_Gr', 46, 6),
                       ('BSun_BK_Mean_Gb', 46, 6),
                       ('BSun_BK_Mean_B', 46, 6),
                       ('BSun_BK_StdDEV_R', 46, 6),
                       ('BSun_BK_StdDEV_Gr', 46, 6),
                       ('BSun_BK_StdDEV_Gb', 46, 6),
                       ('BSun_BK_StdDEV_B', 46, 6),

                       ('DVP27M30F_LMFlip_Cap', 96, 5),
                       ('LMFlip_LT_DRow_R', 58, 4),
                       ('LMFlip_LT_DRow_Gr', 58, 4),
                       ('LMFlip_LT_DRow_Gb', 58, 4),
                       ('LMFlip_LT_DRow_B', 58, 4),
                       ('LMFlip_LT_DCol_R', 57, 4),
                       ('LMFlip_LT_DCol_Gr', 57, 4),
                       ('LMFlip_LT_DCol_Gb', 57, 4),
                       ('LMFlip_LT_DCol_B', 57, 4),
                       ('LMFlip_LT_DRow_Color', 58, 4),
                       ('LMFlip_LT_DCol_Color', 57, 4),
                       ('LMFlip_LT_WeakLineRow_R', 58, 4),
                       ('LMFlip_LT_WeakLineRow_Gr', 58, 4),
                       ('LMFlip_LT_WeakLineRow_Gb', 58, 4),
                       ('LMFlip_LT_WeakLineRow_B', 58, 4),
                       ('LMFlip_LT_WeakLineCol_R', 57, 4),
                       ('LMFlip_LT_WeakLineCol_Gr', 57, 4),
                       ('LMFlip_LT_WeakLineCol_Gb', 57, 4),
                       ('LMFlip_LT_WeakLineCol_B', 57, 4),
                       ('LMFlip_LT_Mean_R', 56, 4),
                       ('LMFlip_LT_Mean_Gr', 56, 4),
                       ('LMFlip_LT_Mean_Gb', 56, 4),
                       ('LMFlip_LT_Mean_B', 56, 4),
                       ('LMFlip_LT_StdDEV_R', 56, 4),
                       ('LMFlip_LT_StdDEV_Gr', 56, 4),
                       ('LMFlip_LT_StdDEV_Gb', 56, 4),
                       ('LMFlip_LT_StdDEV_B', 56, 4),
                       ('LMFlip_LT_RI_R', 56, 4),
                       ('LMFlip_LT_RI_Gr', 56, 4),
                       ('LMFlip_LT_RI_Gb', 56, 4),
                       ('LMFlip_LT_RI_B', 56, 4),
                       ('LMFlip_LT_Ratio_GrR', 56, 4),
                       ('LMFlip_LT_Ratio_GbR', 56, 4),
                       ('LMFlip_LT_Ratio_GrB', 56, 4),
                       ('LMFlip_LT_Ratio_GbB', 56, 4),
                       ('LMFlip_LT_Ratio_GbGr', 56, 4),
                       ('LMFlip_LT_LostBit', 56, 4),
                       ('LMFlip_LT_LostBitSNR_SumDIFF_R', 56, 4),
                       ('LMFlip_LT_LostBitSNR_SumDIFF_Gr', 56, 4),
                       ('LMFlip_LT_LostBitSNR_SumDIFF_Gb', 56, 4),
                       ('LMFlip_LT_LostBitSNR_SumDIFF_B', 56, 4),

                       ('LT_CornerLine', 26, 4),
                       ('LT_ScratchLine', 26, 4),
                       ('LT_Blemish', 31, 4),
                       ('LT_LineStripe', 27, 4),
                       ('LT_Particle', 32, 4),
                       ('BK_Cluster2', 30, 4),  # 4/8
                       ('LT_Cluster2', 30, 4),  # 4/8
                       ('BK_Cluster1', 29, 4),  # 4/8
                       ('LT_Cluster1', 29, 4),  # 4/8
                       ('BK_Cluster3GrGb', 39, 4),  # 4/8
                       ('LT_Cluster3GrGb', 40, 4),  # 4/8
                       ('BK_Cluster3SubtractGrGb', 33, 4),  # 4/8
                       ('LT_Cluster3SubtractGrGb', 34, 4),  # 4/8
                       ('WP_Count', 35, 4),  # 6/8

                       ('BK_Z1_BT_DP_R', 60, 6),
                       ('BK_Z1_BT_DP_Gr', 60, 6),
                       ('BK_Z1_BT_DP_Gb', 60, 6),
                       ('BK_Z1_BT_DP_B', 60, 6),
                       ('BK_Z2_BT_DP_R', 60, 6),
                       ('BK_Z2_BT_DP_Gr', 60, 6),
                       ('BK_Z2_BT_DP_Gb', 60, 6),
                       ('BK_Z2_BT_DP_B', 60, 6),
                       ('BK_Z1_BT_WP_R', 60, 6),
                       ('BK_Z1_BT_WP_Gr', 60, 6),
                       ('BK_Z1_BT_WP_Gb', 60, 6),
                       ('BK_Z1_BT_WP_B', 60, 6),
                       ('BK_Z2_BT_WP_R', 60, 6),
                       ('BK_Z2_BT_WP_Gr', 60, 6),
                       ('BK_Z2_BT_WP_Gb', 60, 6),
                       ('BK_Z2_BT_WP_B', 60, 6),
                       ('LT_Z1_BT_DP_R', 60, 6),
                       ('LT_Z1_BT_DP_Gr', 60, 6),
                       ('LT_Z1_BT_DP_Gb', 60, 6),
                       ('LT_Z1_BT_DP_B', 60, 6),
                       ('LT_Z2_BT_DP_R', 60, 6),
                       ('LT_Z2_BT_DP_Gr', 60, 6),
                       ('LT_Z2_BT_DP_Gb', 60, 6),
                       ('LT_Z2_BT_DP_B', 60, 6),
                       ('LT_Z1_BT_WP_R', 60, 6),
                       ('LT_Z1_BT_WP_Gr', 60, 6),
                       ('LT_Z1_BT_WP_Gb', 60, 6),
                       ('LT_Z1_BT_WP_B', 60, 6),
                       ('LT_Z2_BT_WP_R', 60, 6),
                       ('LT_Z2_BT_WP_Gr', 60, 6),
                       ('LT_Z2_BT_WP_Gb', 60, 6),
                       ('LT_Z2_BT_WP_B', 60, 6),
                       ('LT_Z1_DK_WP_R', 60, 6),
                       ('LT_Z1_DK_WP_Gr', 60, 6),
                       ('LT_Z1_DK_WP_Gb', 60, 6),
                       ('LT_Z1_DK_WP_B', 60, 6),
                       ('LT_Z2_DK_WP_R', 60, 6),
                       ('LT_Z2_DK_WP_Gr', 60, 6),
                       ('LT_Z2_DK_WP_Gb', 60, 6),
                       ('LT_Z2_DK_WP_B', 60, 6),
                       ('LT_Z1_DK_DP_R', 60, 6),
                       ('LT_Z1_DK_DP_Gr', 60, 6),
                       ('LT_Z1_DK_DP_Gb', 60, 6),
                       ('LT_Z1_DK_DP_B', 60, 6),
                       ('LT_Z2_DK_DP_R', 60, 6),
                       ('LT_Z2_DK_DP_Gr', 60, 6),
                       ('LT_Z2_DK_DP_Gb', 60, 6),
                       ('LT_Z2_DK_DP_B', 60, 6),
                       ('BK_Z1_BT_DP', 60, 6),
                       ('BK_Z2_BT_DP', 60, 6),
                       ('BK_Z1_BT_WP', 60, 6),
                       ('BK_Z2_BT_WP', 60, 6),
                       ('LT_Z1_BT_DP', 60, 6),
                       ('LT_Z2_BT_DP', 60, 6),
                       ('LT_Z1_BT_WP', 60, 6),
                       ('LT_Z2_BT_WP', 60, 6),
                       ('LT_Z1_DK_DP', 60, 6),
                       ('LT_Z2_DK_DP', 60, 6),
                       ('LT_Z1_DK_WP', 60, 6),
                       ('LT_Z2_DK_WP', 60, 6),

                       ('DVP27M30F_BK32X_Cap', 98, 5),
                       ('BK32X_BK_BadPixel_Area', 75, 4),
                       ('BK32X_BK_MixDCol_DashQty_R', 51, 6),
                       ('BK32X_BK_MixDCol_DashQty_Gr', 51, 6),
                       ('BK32X_BK_MixDCol_DashQty_Gb', 51, 6),
                       ('BK32X_BK_MixDCol_DashQty_B', 51, 6),
                       ('BK32X_SP_BK_MixDCol_DashQty_R', 54, 2),
                       ('BK32X_SP_BK_MixDCol_DashQty_Gr', 54, 2),
                       ('BK32X_SP_BK_MixDCol_DashQty_Gb', 54, 2),
                       ('BK32X_SP_BK_MixDCol_DashQty_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_DeltaAvg_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_DeltaAvg_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_DeltaAvg_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue0_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue0_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue0_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue0_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue1_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue1_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue1_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue1_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue2_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue2_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue2_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue2_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue3_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue3_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue3_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue3_B', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue4_R', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue4_Gr', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue4_Gb', 54, 2),
                       ('BK32X_BK_MixDCol_DASH_MaxValue4_B', 54, 2),
                       ('BK32X_BK_Mean_R', 53, 2),
                       ('BK32X_BK_Mean_Gr', 53, 2),
                       ('BK32X_BK_Mean_Gb', 53, 2),
                       ('BK32X_BK_Mean_B', 53, 2),
                       ('BK32X_BK_StdDEV_R', 53, 2),
                       ('BK32X_BK_StdDEV_Gr', 53, 2),
                       ('BK32X_BK_StdDEV_Gb', 53, 2),
                       ('BK32X_BK_StdDEV_B', 53, 2),
                       ('BK_Cluster3_2', 73, 2),
                       ('LT_Cluster3_2', 74, 2),

                       ('MIPI2L24M30F_WK1_Cap', 89, 1),
                       ('MIPI_One_W1_FixedPattern', 94, 1),
                       # ('MIPI2L24M30F_WK1_Protocol1', 94, 1),
                       # ('MIPI2L24M30F_WK1_Protocol2', 94, 1),
                       # ('MIPI2L24M30F_WK1_Protocol3', 94, 1),
                       # ('MIPI2L24M30F_WK1_Skew', 94, 1),
                       # ('MIPI2L24M30F_WK1_ErrCnt', 94, 1),



                       ('MIPI2L24M30F_LT_Cap', 90, 1),
                       # ('MIPI2L24M30F_LT_Protocol1', 94, 1),
                       # ('MIPI2L24M30F_LT_Protocol2', 94, 1),
                       # ('MIPI2L24M30F_LT_Protocol3', 94, 1),
                       # ('MIPI2L24M30F_LT_Skew', 94, 1),
                       ('MIPI_LT_DRow_R', 65, 1),
                       ('MIPI_LT_DRow_Gr', 65, 1),
                       ('MIPI_LT_DRow_Gb', 65, 1),
                       ('MIPI_LT_DRow_B', 65, 1),
                       ('MIPI_LT_DCol_R', 64, 1),
                       ('MIPI_LT_DCol_Gr', 64, 1),
                       ('MIPI_LT_DCol_Gb', 64, 1),
                       ('MIPI_LT_DCol_B', 64, 1),
                       ('MIPI_LT_DRow_Color', 65, 1),
                       ('MIPI_LT_DCol_Color', 64, 1),
                       ('MIPI_LT_WeakLineRow_R', 65, 1),
                       ('MIPI_LT_WeakLineRow_Gr', 65, 1),
                       ('MIPI_LT_WeakLineRow_Gb', 65, 1),
                       ('MIPI_LT_WeakLineRow_B', 65, 1),
                       ('MIPI_LT_WeakLineCol_R', 64, 1),
                       ('MIPI_LT_WeakLineCol_Gr', 64, 1),
                       ('MIPI_LT_WeakLineCol_Gb', 64, 1),
                       ('MIPI_LT_WeakLineCol_B', 64, 1),
                       ('MIPI_LT_Mean_R', 63, 1),
                       ('MIPI_LT_Mean_Gr', 63, 1),
                       ('MIPI_LT_Mean_Gb', 63, 1),
                       ('MIPI_LT_Mean_B', 63, 1),
                       ('MIPI_LT_StdDEV_R', 63, 1),
                       ('MIPI_LT_StdDEV_Gr', 63, 1),
                       ('MIPI_LT_StdDEV_Gb', 63, 1),
                       ('MIPI_LT_StdDEV_B', 63, 1),
                       ('MIPI_LT_RI_R', 63, 1),
                       ('MIPI_LT_RI_Gr', 63, 1),
                       ('MIPI_LT_RI_Gb', 63, 1),
                       ('MIPI_LT_RI_B', 63, 1),
                       ('MIPI_LT_Ratio_GrR', 63, 1),
                       ('MIPI_LT_Ratio_GbR', 63, 1),
                       ('MIPI_LT_Ratio_GrB', 63, 1),
                       ('MIPI_LT_Ratio_GbB', 63, 1),
                       ('MIPI_LT_Ratio_GbGr', 63, 1),
                       ('MIPI_LT_LostBit', 63, 1),
                       ('MIPI_LT_LostBitSNR_SumDIFF_R', 63, 1),
                       ('MIPI_LT_LostBitSNR_SumDIFF_Gr', 63, 1),
                       ('MIPI_LT_LostBitSNR_SumDIFF_Gb', 63, 1),
                       ('MIPI_LT_LostBitSNR_SumDIFF_B', 63, 1),

                       ('MIPI2L24M30F_LBIT_Cap', 90, 1),
                       ('MIPI_LBIT_LT_Mean_R', 63, 1),
                       ('MIPI_LBIT_LT_Mean_Gr', 63, 1),
                       ('MIPI_LBIT_LT_Mean_Gb', 63, 1),
                       ('MIPI_LBIT_LT_Mean_B', 63, 1),
                       ('MIPI_LBIT_LT_LostBit', 63, 1),
                       ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_R', 63, 1),
                       ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gr', 63, 1),
                       ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_Gb', 63, 1),
                       ('MIPI_LBIT_LT_LostBitSNR_SumDIFF_B', 63, 1),

                       ('Binning', 2, 3),
                       ('All Pass', 1, 3)
                       ]]


def parse_file(file, bin_definition):
    """
    解析文件
    :param bin_definition: 分bin定义
    :param file: 文件
    :return: 分bin有问题的数据
    """
    data = []
    with open(file) as f:
        csv_reader = reader(f)
        for row in csv_reader:
            data.append(row)

    search_binning = Common.search_string(data, 'Binning')
    if not search_binning:
        exit()
    else:
        binning_row_num = search_binning[0]
        binning_col_num = search_binning[1]

    col_count = binning_col_num + 1
    first_register_row_num = len(data) - 1
    for i in range(binning_row_num + row_offset, len(data)):
        try:
            int(data[i][0])
        except:
            first_register_row_num = i
            break

    error_message = []
    parse_file_widgets = ['ParseFile: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ',
                          FileTransferSpeed()]
    parse_file_pbar = ProgressBar(widgets=parse_file_widgets, maxval=first_register_row_num).start()
    for row_num in range(binning_row_num + row_offset, first_register_row_num):
        row_softbin_index = len(bin_definition) - 1
        for col_num in range(col_offset, col_count):
            test_item_name = data[binning_row_num][col_num].strip()
            if test_item_name == 'AVDD_O/S':  # JX828测试项特殊处理
                continue
            else:
                high_limit_data = data[binning_row_num + 2][col_num]
                low_limit_data = data[binning_row_num + 3][col_num]
            try:
                high_limit = float(high_limit_data)
                low_limit = float(low_limit_data)
                try:
                    value = data[row_num][col_num]
                    value_convert = float(value)
                    if value_convert == int(value_convert):
                        value_convert = int(value_convert)
                    if value_convert < low_limit or high_limit < value_convert:
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == test_item_name:
                                if row_softbin_index > i:
                                    row_softbin_index = i
                except:
                    for i in range(len(bin_definition)):
                        if bin_definition[i][0] == test_item_name:
                            if row_softbin_index > i - 1:
                                row_softbin_index = i - 1
            except:
                try:
                    value = data[row_num][col_num]
                    float(value)
                    if test_item_name == 'iic_test' and value == '0':
                        for i in range(len(bin_definition)):
                            if bin_definition[i][0] == 'iic_test':
                                if row_softbin_index > i:
                                    row_softbin_index = i
                except:
                    for i in range(len(bin_definition)):
                        if bin_definition[i][0] == test_item_name:
                            if row_softbin_index > i:
                                row_softbin_index = i

        if bin_definition[row_softbin_index][1] != int(data[row_num][2]):
            error_message.append("              ChipNo " + data[row_num][0] + " 的SB_BIN错误：根据优先级计算出来的swbin为 " + str(
                bin_definition[row_softbin_index][1]) + " ,CSV中为 " + data[row_num][2] + "\n")
        if bin_definition[row_softbin_index][2] != int(data[row_num][3]):
            error_message.append("              ChipNo " + data[row_num][0] + " 的hW_BIN错误：根据优先级计算出来的hwbin为 " + str(
                bin_definition[row_softbin_index][2]) + " ,CSV中为 " + data[row_num][3] + "\n")
        if row_num % 1000 == 0 or row_num == first_register_row_num - 1:
            parse_file_pbar.update(row_num + 1)
    parse_file_pbar.finish()
    return error_message


def save_data(file, result_file, error_message):
    """
    保存数据
    :param file: 解析的文件路径
    :param result_file: 写结果文件
    :param error_message: 分bin有问题的数据
    :return: 
    """
    file_name = basename(file)
    with open(result_file, 'a') as f:
        f.write("            " + file_name + "：\n")
        if len(error_message) > 0:
            for item in error_message:
                f.write(item)
        else:
            f.write('              分Bin没有问题。\n')


def main():
    # Date folder path
    if argv.count('-d') == 0:
        print("Error：Date folder path为必填项，格式：“-d D:\date folder”。")
        exit()
    else:
        date_folder = argv[argv.index('-d') + 1]
        for i in range(argv.index('-d') + 2, len(argv)):
            if not argv[i].startswith('-'):
                date_folder += (' ' + argv[i])
            else:
                break

    # 项目 0:F28,1:JX828
    if argv.count('-p') != 0:
        project_id = int(argv[argv.index('-p') + 1])
    else:
        project_id = 0  # 默认F28项目

    lotno_names = listdir(date_folder)
    for name in lotno_names:
        folder = join(date_folder, name)
        if isdir(folder):
            file_list = Common.get_filelist(folder, '.csv')
            if not file_list:
                exit()
            # Analysis folder path
            if argv.count('-a') == 0:
                analysis_folder = folder + '\Analysis'
            else:
                analysis_folder = argv[argv.index('-a') + 1]

            Common.mkdir(analysis_folder)
            date = datetime.now().strftime("%Y%m%d%H%M")
            result_file = join(analysis_folder, 'BinningCheck' + date + '.txt')

            for file in file_list:
                print(file)
                # parse file
                error_message = parse_file(file, bin_definition[project_id])
                # save data
                save_data(file, result_file, error_message)


if __name__ == '__main__':
    main()
