Datalog_Analysis.py
	功能
		对datalog csv文件中测试项是否在Limit范围内进行分析
	模式
		DateFolder：某个日期所在文件夹，如20190924文件夹
		LotFolder：某个批次所在文件夹，如BRN245000#13文件夹
		SingleFile：单个csv文件，如Lot_BRN245000#13_FT.csv文件
	步骤
		1.选择一个模式，点击Open
		2.选择对应的文件夹或文件，程序会尝试从csv中获取如下数据：
			HiLimitRowNum：行首为“MAX”的行号
			LoLimitRowNum：行首为“MIN”的行号
			TestDataRowNum：行号从小到大检索行首，直到第一个int类型数据所在的行号
			TestDataColLetter：列号从小到大检索TestDataRowNum所在行，直到第一个float类型数据所在的列名（大写字母）
			TestItemRowNum：行首为“ChipNo”的行号
		3.若勾选AllTestData，即所有测试项；若取消勾选AllTestData，需要输入测试项的起止列列名（大写字母）
		4.点击Analysis
	结果
		一个csv文件对应生成一个excel文件，存放于csv文件同级的Analysis文件夹中
			待分析测试项的MAX和MIN标绿
			超过Limit的数据标红，空值标紫
			ChipNo所在行，如果存在超过Limit的数据， ChipNo标红并在其后用小括号保存超过Limit的个数
			待分析测试项所在列，如果存在超过Limit的数据， 该测试项标黄并在其后用小括号保存超过Limit的个数

Datalog_DateLot_Analysis.py
	功能
		对datalog csv文件进行分析Summary、DataCheck、BinningCheck和NanChipno
		支持项目：F28、JX828、JX825、JX832
	模式
		DateFolder：某个日期所在文件夹，如20191114文件夹
		LotFolder：某个批次所在文件夹，如BRR741000#17-20文件夹
	步骤
		1.选择一个模式，点击Open
		2.选择对应的文件夹
		3.选择项目
		4.选择待分析的项目（All表示所有项目）
		5.点击Analysis
	结果
		结果文件存放于csv文件同级的Analysis文件夹中
		Summary
			HWBin：对某个批次的Hard Bin进行良率的分析统计
			HWBin-SWBin：对某个批次Hard Bin下Soft Bin进行分析统计
			Site-SWBin：对某个批次Site对应Soft Bin进行分析统计
			HWBin-TestItem：对某个批次Hard Bin对应TestItem进行分析统计
			SWBin-TestItem：对某个批次Soft Bin对应TestItem进行分析统计
			Site-TestItem：对某个批次Site对应TestItem进行分析统计
		DataCheck
			在.csv文件基础上分析异常测试结果
				红色背景：超出Limit范围
				黄色背景：iic_test的值不是1
				紫色背景：空值及其对应的ChipNo
		BinningCheck
			对某个批次分bin正确性进行校验分析
		NanChipno
			对某个批次的DC和Image测试项为空值进行分析统计
	
Datalog_Total_Analysis.py
	功能
		对所有批次的datalog csv文件进行整体分析统计
		支持项目：F28、JX828、JX825、JX832
	模式
		ProjectFolder：某个项目所在文件夹，如JX828文件夹
		HandlerFolder：某个Handler所在文件夹，如828_2#文件夹
	步骤
		1.选择一个模式，点击Open
		2.选择对应的文件夹
		3.选择项目
		4.点击Analysis
	结果
		结果文件存放于Handler文件夹同级的Analysis文件夹中
			Site-SWBin：对所有批次的Site对应Soft Bin的分析统计
			LotNo-SWBin：对每个批次对应Soft Bin的分析统计