RepeatabilityTest.py
	功能
		对csv文件中的数据进行删选
	模式
		SourceFolder：csv所在的文件夹
		SingleFile：单个csv文件
		Delete continuous duplicate data：删除连续重复的数据
	步骤
		1.选择一个模式，点击Open
		2.选择对应的文件夹或文件
		3.点击Analysis
	结果
		结果文件存放于csv文件同级的Analysis文件夹中
			勾选了Delete continuous duplicate data
				在源文件的基础上，删除连续重复的数据
			未勾选Delete continuous duplicate data
				计算每个组的最大值，并计算出所有组的最小值、最大值、平均值、cp20和cp15