Datalog_Analysis.py
	����
		��datalog csv�ļ��в������Ƿ���Limit��Χ�ڽ��з���
	ģʽ
		DateFolder��ĳ�����������ļ��У���20190924�ļ���
		LotFolder��ĳ�����������ļ��У���BRN245000#13�ļ���
		SingleFile������csv�ļ�����Lot_BRN245000#13_FT.csv�ļ�
	����
		1.ѡ��һ��ģʽ�����Open
		2.ѡ���Ӧ���ļ��л��ļ�������᳢�Դ�csv�л�ȡ�������ݣ�
			HiLimitRowNum������Ϊ��MAX�����к�
			LoLimitRowNum������Ϊ��MIN�����к�
			TestDataRowNum���кŴ�С����������ף�ֱ����һ��int�����������ڵ��к�
			TestDataColLetter���кŴ�С�������TestDataRowNum�����У�ֱ����һ��float�����������ڵ���������д��ĸ��
			TestItemRowNum������Ϊ��ChipNo�����к�
		3.����ѡAllTestData�������в������ȡ����ѡAllTestData����Ҫ������������ֹ����������д��ĸ��
		4.���Analysis
	���
		һ��csv�ļ���Ӧ����һ��excel�ļ��������csv�ļ�ͬ����Analysis�ļ�����
			�������������MAX��MIN����
			����Limit�����ݱ�죬��ֵ����
			ChipNo�����У�������ڳ���Limit�����ݣ� ChipNo��첢�������С���ű��泬��Limit�ĸ���
			�����������������У�������ڳ���Limit�����ݣ� �ò������Ʋ��������С���ű��泬��Limit�ĸ���

Datalog_DateLot_Analysis.py
	����
		��datalog csv�ļ����з���Summary��DataCheck��BinningCheck��NanChipno
		֧����Ŀ��F28��JX828��JX825��JX832
	ģʽ
		DateFolder��ĳ�����������ļ��У���20191114�ļ���
		LotFolder��ĳ�����������ļ��У���BRR741000#17-20�ļ���
	����
		1.ѡ��һ��ģʽ�����Open
		2.ѡ���Ӧ���ļ���
		3.ѡ����Ŀ
		4.ѡ�����������Ŀ��All��ʾ������Ŀ��
		5.���Analysis
	���
		����ļ������csv�ļ�ͬ����Analysis�ļ�����
		Summary
			HWBin����ĳ�����ε�Hard Bin�������ʵķ���ͳ��
			HWBin-SWBin����ĳ������Hard Bin��Soft Bin���з���ͳ��
			Site-SWBin����ĳ������Site��ӦSoft Bin���з���ͳ��
			HWBin-TestItem����ĳ������Hard Bin��ӦTestItem���з���ͳ��
			SWBin-TestItem����ĳ������Soft Bin��ӦTestItem���з���ͳ��
			Site-TestItem����ĳ������Site��ӦTestItem���з���ͳ��
		DataCheck
			��.csv�ļ������Ϸ����쳣���Խ��
				��ɫ����������Limit��Χ
				��ɫ������iic_test��ֵ����1
				��ɫ��������ֵ�����Ӧ��ChipNo
		BinningCheck
			��ĳ�����η�bin��ȷ�Խ���У�����
		NanChipno
			��ĳ�����ε�DC��Image������Ϊ��ֵ���з���ͳ��
	
Datalog_Total_Analysis.py
	����
		���������ε�datalog csv�ļ������������ͳ��
		֧����Ŀ��F28��JX828��JX825��JX832
	ģʽ
		ProjectFolder��ĳ����Ŀ�����ļ��У���JX828�ļ���
		HandlerFolder��ĳ��Handler�����ļ��У���828_2#�ļ���
	����
		1.ѡ��һ��ģʽ�����Open
		2.ѡ���Ӧ���ļ���
		3.ѡ����Ŀ
		4.���Analysis
	���
		����ļ������Handler�ļ���ͬ����Analysis�ļ�����
			Site-SWBin�����������ε�Site��ӦSoft Bin�ķ���ͳ��
			LotNo-SWBin����ÿ�����ζ�ӦSoft Bin�ķ���ͳ��