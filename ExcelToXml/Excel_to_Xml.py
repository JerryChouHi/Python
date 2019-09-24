# encoding:utf-8
# @Time     : 2019/8/9 9:37
# @Author   : Jerry Chou
# @File     : Excel_to_Xml.py
# @Function :

from sys import argv, exit
from os import path, makedirs, getcwd
from xml.dom.minidom import parse
from math import isnan
from pandas import read_excel
from shutil import copy


def mkdir(dir):
    dir = dir.strip()
    dir = dir.rstrip("\\")
    isExists = path.exists(dir)
    if not isExists:
        makedirs(dir)
        # print(path + '创建成功')
        return True
    else:
        # print(path + '目录已存在')
        return False


def write_signals_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<Signals>\n")
    for i in range(len(data)):
        file.write("		<Signal name=\"" + data[i][0] + "\">\n")
        file.write("			<Type>" + data[i][1] + "</Type>\n")
        file.write("			<DutPin>" + str(i + 1) + "</DutPin>\n")
        file.write("		</Signal>\n")
    file.write("	</Signals>\n")
    file.write("</Blocks>")


def write_socketmap_file(data, file, socketmap_name):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<SocketMap name=\"" + socketmap_name + "\">\n")
    file.write("		<Site count=\"" + str(len(data[0]) - 1) + "\">\n")
    file.write("			<Thread>Single</Thread>\n")
    file.write("		</Site>\n")
    for i in range(len(data)):
        file.write("		<SignalRef name=\"" + data[i][0] + "\">\n")
        file.write("			<SocketGrid>")
        for j in range(1, len(data[i])):
            file.write(data[i][j])
            if j < len(data[i]) - 1:
                file.write(" ")
        file.write("</SocketGrid>\n")
        file.write("		</SignalRef>\n")
    file.write("	</SocketMap>\n")
    file.write("</Blocks>")


def write_signalgroups_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<Signalgroups>\n")
    for i in range(len(data)):
        file.write("		<Signalgroup name=\"" + data[i][0] + "\">\n")
        file.write("			<Type>" + data[i][1] + "</Type>\n")
        file.write("			<SigRefExpression>" + data[i][2] + "</SigRefExpression>\n")
        file.write("		</Signalgroup>\n")
    file.write("	</Signalgroups>\n")
    file.write("</Blocks>")


def write_bindefinition_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<CountGroup>\n")
    file.write("		<Count name=\"Pass\">\n")
    file.write("			<Value>PassCount</Value>\n")
    file.write("		</Count>\n")
    file.write("		<Count name=\"Fail\">\n")
    file.write("			<Value>FailCount</Value>\n")
    file.write("		</Count>\n")
    file.write("	</CountGroup>\n")
    file.write("	<BinDefs name=\"Default\">\n")
    file.write("		<BinGroup name=\"PassFailBins\" type=\"PassFailBin\">\n")
    file.write("			<Bin name=\"Pass\">\n")
    file.write("				<ID>0</ID>\n")
    file.write("				<Desc>Count of passing DUTS</Desc>\n")
    file.write("			</Bin>\n")
    file.write("			<Bin name=\"Fail\">\n")
    file.write("				<ID>1</ID>\n")
    file.write("				<Desc>Count of falling DUTS</Desc>\n")
    file.write("			</Bin>\n")
    file.write("		</BinGroup>\n")
    file.write("		<BinGroup name=\"HardBins\" type=\"HardBin\">\n")
    for i in range(len(data[1])):
        file.write("			<Bin name=\"" + str(data[1][i][1]) + "\">\n")
        file.write("				<ID>" + str(int(data[1][i][0])) + "</ID>\n")
        file.write("				<Desc>" + str(data[1][i][3]) + "</Desc>\n")
        file.write("				<Inherit>" + str(data[1][i][2]) + "</Inherit>\n")
        file.write("			</Bin>\n")
    file.write("		</BinGroup>\n")
    file.write("		<BinGroup name=\"SoftBins\" type=\"SoftBin\">\n")
    for i in range(len(data[0])):
        file.write("			<Bin name=\"" + str(data[0][i][1]) + "\">\n")
        file.write("				<ID>" + str(int(data[0][i][0])) + "</ID>\n")
        file.write("				<Desc>" + str(data[0][i][2]) + "</Desc>\n")
        file.write("				<Inherit>" + str(data[1][data[0][i][3] - 1][1]) + "</Inherit>\n")
        file.write("			</Bin>\n")
    file.write("		</BinGroup>\n")
    file.write("	</BinDefs>\n")
    file.write("</Blocks>")


def write_limit_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    for i in range(len(data)):
        file.write("	<Limit name=\"" + data[i][1] + "\">\n")
        file.write("		<TestNum>" + str(data[i][0]) + "</TestNum>\n")
        file.write("		<LoLimit>" + str(data[i][3]) + "</LoLimit>\n")
        file.write("		<HiLimit>" + str(data[i][2]) + "</HiLimit>\n")
        if data[i][4] != '':
            file.write("		<Unit>" + data[i][4] + "</Unit>\n")
        if data[i][5] != '':
            file.write(
                "		<SoftBinRef binRef=\"Default\" group=\"SoftBins\">" + str(data[i][5]) + "</SoftBinRef>\n")
        if data[i][6] != '':
            file.write("		<Description>" + str(data[i][6]) + "</Description>\n")
        file.write("	</Limit>\n")
    file.write("</Blocks>")


def write_block_file(data, file, socketmap_name):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<DCMeasures>\n")
    for i in range(len(data[0])):
        file.write("		<DCMeasure name=\"" + data[0][i][0] + "\">\n")
        for j in range(1, len(data[0][i])):
            file.write("			<MeasureGroup sigRef=\"" + data[0][i][j][0] + "\" minorTestNum=\"" + str(
                int(data[0][i][j][1])) + "\">\n")
            file.write("				<Mode>" + data[0][i][j][2] + "</Mode>\n")
            file.write("				<Method>" + data[0][i][j][3] + "</Method>\n")
            file.write("				<ForceValue>" + data[0][i][j][4] + "</ForceValue>\n")
            file.write("				<Range>" + data[0][i][j][5] + "</Range>\n")
            file.write("				<HiLimit>" + data[0][i][j][6] + "</HiLimit>\n")
            file.write("				<LoLimit>" + data[0][i][j][7] + "</LoLimit>\n")
            if data[0][i][j][8]:
                file.write("				<HiClamp>" + data[0][i][j][8] + "</HiClamp>\n")
            if data[0][i][j][9]:
                file.write("				<LoClamp>" + data[0][i][j][9] + "</LoClamp>\n")
            if data[0][i][j][10]:
                file.write("				<SampleNum>" + str(int(data[0][i][j][10])) + "</SampleNum>\n")
            if data[0][i][j][11]:
                file.write("				<Delay>" + data[0][i][j][11] + "</Delay>\n")
            file.write("			</MeasureGroup>\n")
        file.write("		</DCMeasure>\n")
    file.write("	</DCMeasures>\n")
    file.write("	<TestConditions>\n")
    file.write("		<TestCondition name=\"PowerOn\">\n")
    file.write("			<LevelRef>PowerOn</LevelRef>\n")
    file.write("		</TestCondition>\n")
    file.write("		<TestCondition name=\"PowerOff\">\n")
    file.write("			<LevelRef>PowerOff</LevelRef>\n")
    file.write("		</TestCondition>\n")
    file.write("		<TestCondition name=\"General\">\n")
    file.write("			<LevelRef>General</LevelRef>\n")
    file.write("		</TestCondition>\n")
    file.write("		<TestCondition name=\"SocketMapCheck\"/>\n")
    file.write("		<TestCondition name=\"LoadAllPats\"/>\n")
    file.write("		<TestCondition name=\"InstrumentInit\"/>\n")
    file.write("		<TestCondition name=\"TestProgramCheck\"/>\n")
    file.write("		<TestCondition name=\"TurboModeInit\"/>\n")
    for i in range(len(data[1])):
        file.write("		<TestCondition name=\"" + data[1][i][0] + "\"/>\n")
    file.write("	</TestConditions>\n")
    file.write("	<Tests>\n")
    file.write("		<Test name=\"SocketMapCheck\" testNum=\"500\">\n")
    file.write("			<TestCondition>SocketMapCheck</TestCondition>\n")
    file.write("			<ExecAPI>test_template\init\SocketMapValidate</ExecAPI>\n")
    file.write("			<Param name=\"SocketMap\">\n")
    file.write("				<Type>SocketMap</Type>\n")
    file.write("				<Value>" + socketmap_name + "</Value>\n")
    file.write("			</Param>\n")
    file.write("		</Test>\n")
    file.write("		<Test name=\"LoadAllPats\" testNum=\"500\">\n")
    file.write("			<TestCondition>LoadAllPats</TestCondition>\n")
    file.write("			<ExecAPI>test_template\Init\PatternLoader</ExecAPI>\n")
    file.write("		</Test>\n")
    file.write("		<Test name=\"InstrumentInit\" testNum=\"500\">\n")
    file.write("			<TestCondition>InstrumentInit</TestCondition>\n")
    file.write("			<ExecAPI>test_template\Init\InstrumentInit</ExecAPI>\n")
    file.write("			<Param name=\"LoadCalibration\">\n")
    file.write("				<Type>Value_Single</Type>\n")
    file.write("				<Value>0</Value>\n")
    file.write("			</Param>\n")
    file.write("		</Test>\n")
    file.write("		<Test name=\"TestProgramCheck\" testNum=\"500\">\n")
    file.write("			<TestCondition>TestProgramCheck</TestCondition>\n")
    file.write("			<ExecAPI>test_templates\init\TestProgramValidate</ExecAPI>\n")
    file.write("		</Test>\n")
    file.write("		<Test name=\"TurboModeInit\" testNum=\"500\">\n")
    file.write("			<TestCondition>TurboModeInit</TestCondition>\n")
    file.write("			<ExecAPI>test_template\Init\TurboModeInit</ExecAPI>\n")
    file.write("		</Test>\n")
    for i in range(len(data[1])):
        file.write("		<Test name=\"" + data[1][i][0] + "\" testNum=\"" + str(data[1][i][1]) + "\">\n")
        file.write("			<TestCondition>" + data[1][i][0] + "</TestCondition>\n")
        file.write("			<ExecAPI>" + data[1][i][2] + "</ExecAPI>\n")
        if data[1][i][3] != '':
            file.write("			<Param name=\"" + data[1][i][3] + "\">\n")
            if data[1][i][3] in ['DCMeasure', 'SocketMap', 'PatternBurst']:
                file.write("				<Type>" + data[1][i][3] + "</Type>\n")
            else:
                file.write("				<Type>Value_String</Type>\n")
            file.write("				<Value>" + data[1][i][4] + "</Value>\n")
            file.write("			</Param>\n")
        file.write("		</Test>\n")
    file.write("	</Tests>\n")
    file.write("</Blocks>")


def write_uservars_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<UserVars>\n")
    for i in range(len(data)):
        file.write("		<Variable name=\"" + data[i][0] + "\" type=\"" + data[i][1] + "\">\n")
        file.write("			<Value>" + data[i][2] + "</Value>\n")
        file.write("		</Variable>\n")
    file.write("	</UserVars>\n")
    file.write("</Blocks>")


def write_levels_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    for i in range(len(data)):
        file.write("	<Levels name=\"" + data[i][0] + "\">\n")
        for j in range(1, len(data[i])):
            file.write("		<SigRef name=\"" + data[i][j][0] + "\">\n")
            if data[i][j][1] != '':
                file.write("			<VPS>" + str(data[i][j][1]) + "</VPS>\n")
            if data[i][j][2] != '':
                file.write("			<IClamp>" + str(data[i][j][2]) + "</IClamp>\n")
            if data[i][j][3] != '':
                file.write("			<IRange>" + str(int(data[i][j][3])) + "</IRange>\n")
            if data[i][j][4] != '':
                file.write("			<Delay>" + data[i][j][4] + "</Delay>\n")
            if data[i][j][5] != '':
                file.write("			<VIL>" + str(data[i][j][5]) + "</VIL>\n")
            if data[i][j][6] != '':
                file.write("			<VIH>" + str(data[i][j][6]) + "</VIH>\n")
            if data[i][j][7] != '':
                file.write("			<VTERM>" + str(data[i][j][7]) + "</VTERM>\n")
            if data[i][j][8] != '':
                file.write("			<VTERM_EN>" + str(int(data[i][j][8])) + "</VTERM_EN>\n")
            if data[i][j][9] != '':
                file.write("			<VOL>" + str(data[i][j][9]) + "</VOL>\n")
            if data[i][j][10] != '':
                file.write("			<VOH>" + str(data[i][j][10]) + "</VOH>\n")
            if data[i][j][11] != '':
                file.write("			<VCH>" + str(data[i][j][11]) + "</VCH>\n")
            if data[i][j][12] != '':
                file.write("			<VCL>" + str(data[i][j][12]) + "</VCL>\n")
            file.write("		</SigRef>\n")
        file.write("	</Levels>\n")
    file.write("</Blocks>")


def write_project_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<Project>\n")
    file.write("		<TesterConfig>\n")
    file.write("			<FilePath>XML\TesterConfig.xml</FilePath>\n")
    file.write("		</TesterConfig>\n")
    file.write("		<Signals>\n")
    file.write("			<FilePath>XML\Signals.xml</FilePath>\n")
    file.write("		</Signals>\n")
    file.write("		<SocketMap>\n")
    file.write("			<FilePath>XML\SocketMap.xml</FilePath>\n")
    file.write("			<Ref>SocketMap</Ref>\n")
    file.write("		</SocketMap>\n")
    file.write("		<SignalGroups>\n")
    file.write("			<FilePath>XML\SignalGroups.xml</FilePath>\n")
    file.write("		</SignalGroups>\n")
    file.write("		<BinDefinition>\n")
    file.write("			<FilePath>XML\BinDefinition.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</BinDefinition>\n")
    file.write("		<TestItemLimit>\n")
    file.write("			<FilePath>XML\Limit.xml</FilePath>\n")
    file.write("		</TestItemLimit>\n")
    file.write("		<UserVars>\n")
    file.write("			<FilePath>XML\\UserVars.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</UserVars>\n")
    file.write("		<SpecSet>\n")
    file.write("			<FilePath>XML\SpecSet.xml</FilePath>\n")
    file.write("			<Ref>Setting1</Ref>\n")
    file.write("		</SpecSet>\n")
    file.write("		<Levels>\n")
    file.write("			<FilePath>XML\Levels.xml</FilePath>\n")
    file.write("			<Ref>Dctest1</Ref>\n")
    file.write("		</Levels>\n")
    file.write("		<Timing>\n")
    file.write("			<FilePath>XML\Timing.xml</FilePath>\n")
    file.write("			<Ref>Tim1</Ref>\n")
    file.write("		</Timing>\n")
    file.write("		<TimingMap>\n")
    file.write("			<FilePath>XML\TimingMap.xml</FilePath>\n")
    file.write("			<Ref>TMap1</Ref>\n")
    file.write("		</TimingMap>\n")
    file.write("		<PatternBurst>\n")
    file.write("			<FilePath>XML\PatternBurst.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</PatternBurst>\n")
    file.write("		<TestBlock>\n")
    file.write("			<FilePath>XML\TestBlock.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</TestBlock>\n")
    file.write("		<Flows>\n")
    file.write("			<FilePath>XML\Flows.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</Flows>\n")
    file.write("		<TestProgram>\n")
    file.write("			<FilePath>XML\TestProgram.xml</FilePath>\n")
    file.write("			<Ref>name</Ref>\n")
    file.write("		</TestProgram>\n")
    file.write("		<RunResultMap>\n")
    file.write("			<FilePath>XML\RunResultMap.xml</FilePath>\n")
    file.write("		</RunResultMap>\n")
    file.write("		<Shmoo>\n")
    file.write("			<FilePath>XML\Shmoo.xml</FilePath>\n")
    file.write("		</Shmoo>\n")
    file.write("	</Project>\n")
    file.write("	<Datalog>\n")
    file.write("		<SeparateLog>\n")
    file.write("			<Enable>true</Enable>\n")
    file.write("			<Manual>Manual_%s</Manual>\n")
    file.write("			<Lot>Lot_%s</Lot>\n")
    file.write("		</SeparateLog>\n")
    file.write("	</Datalog>\n")
    file.write("</Blocks>")


def write_config_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<TesterConfig>\n")
    file.write("		<Chassis id=\"0\">\n")
    file.write("			<Tester name=\"FirstTester\">\n")
    file.write("				<Instrument slot=\"0\" type=\"Shark\" name=\"Shark0\" version=\"1.0.0\"/>\n")
    file.write("				<Instrument slot=\"1\" type=\"Shark\" name=\"Shark1\" version=\"1.0.0\"/>\n")
    file.write("				<Instrument slot=\"4\" type=\"Shark\" name=\"Shark4\" version=\"1.0.0\"/>\n")
    file.write("				<Instrument slot=\"5\" type=\"Shark\" name=\"Shark5\" version=\"1.0.0\"/>\n")
    file.write("			</Tester>\n")
    file.write("		</Chassis>\n")
    file.write("	</TesterConfig>\n")
    file.write("</Blocks>")


def write_program_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<TestProgram>\n")
    file.write("		<Task name=\"Install\">\n")
    file.write("			<Type>Install</Type>\n")
    file.write("			<Thread>Single</Thread>\n")
    file.write("			<FlowRef>INSTALL_FLOW</FlowRef>\n")
    file.write("		</Task>\n")
    file.write("		<Task name=\"Init\">\n")
    file.write("			<Type>SocketBoard</Type>\n")
    file.write("			<Thread>Multi</Thread>\n")
    file.write("			<FlowRef>INIT_FLOW</FlowRef>\n")
    file.write("		</Task>\n")
    file.write("		<Task name=\"Start\">\n")
    file.write("			<Type>DUT</Type>\n")
    file.write("			<Thread>Multi</Thread>\n")
    file.write("			<FlowRef>MAIN_FLOW</FlowRef>\n")
    file.write("		</Task>\n")
    file.write("		<Task name=\"Alarm\">\n")
    file.write("			<Type>Alarm</Type>\n")
    file.write("			<Thread>Multi</Thread>\n")
    file.write("			<FlowRef>ALARM_FLOW</FlowRef>\n")
    file.write("		</Task>\n")
    file.write("		<Task name=\"PowerDown\">\n")
    file.write("			<Type>PowerDown</Type>\n")
    file.write("			<Thread>Multi</Thread>\n")
    file.write("			<FlowRef>POWERDOWN_FLOW</FlowRef>\n")
    file.write("		</Task>\n")
    file.write("	</TestProgram>\n")
    file.write("</Blocks>")


def write_shmoo_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<Axes>\n")
    file.write("        <Axis name=\"tper_axis\">\n")
    file.write("            <Type>UserVar</Type>\n")
    file.write("            <Target>TPer</Target>\n")
    file.write("            <Min>10</Min>\n")
    file.write("            <Max>50</Max>\n")
    file.write("			<Steps>5</Steps>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("            <Description>user axis</Description>\n")
    file.write("        </Axis>\n")
    file.write("        <Axis name=\"vdd_axis\">\n")
    file.write("    	    <Type>UserVar</Type>\n")
    file.write("            <Target>VDDTyp</Target>\n")
    file.write("            <Min>0.5</Min>\n")
    file.write("            <Max>1.28</Max>\n")
    file.write("			<Delta>0.4</Delta>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("            <Description>spec axis</Description>\n")
    file.write("        </Axis>\n")
    file.write("        <Axis name=\"avdd_axis\">\n")
    file.write("    	    <Type>UserVar</Type>\n")
    file.write("            <Target>AVDDTyp</Target>\n")
    file.write("            <Min>1.3</Min>\n")
    file.write("            <Max>2.9</Max>\n")
    file.write("			<Steps>2</Steps>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("        </Axis>\n")
    file.write("        <Axis name=\"tperSpec_axis\">\n")
    file.write("    	    <Type>SpecVar</Type>\n")
    file.write("            <Target>tperSpec</Target>\n")
    file.write("            <Min>10</Min>\n")
    file.write("            <Max>50</Max>\n")
    file.write("			<Steps>21</Steps>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("        </Axis>\n")
    file.write("        <Axis name=\"vddSpec_axis\">\n")
    file.write("    	    <Type>Level</Type>\n")
    file.write("            <Target>DVDD.VPS</Target>\n")
    file.write("            <Min>0.5</Min>\n")
    file.write("            <Max>1.28</Max>\n")
    file.write("			<Steps>5</Steps>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("        </Axis>\n")
    file.write("        <Axis name=\"avddSpec_axis\">\n")
    file.write("    	    <Type>Level</Type>\n")
    file.write("            <Target>AVDD.VPS</Target>\n")
    file.write("            <Min>1.3</Min>\n")
    file.write("            <Max>2.9</Max>\n")
    file.write("			<Steps>7</Steps>\n")
    file.write("            <Algorithm>Lineal</Algorithm>\n")
    file.write("        </Axis>\n")
    file.write("	</Axes>\n")
    file.write("	<Shmoos>\n")
    file.write("		<Shmoo name=\"shmoo1\">\n")
    file.write("			<XAxis>tper_axis</XAxis>\n")
    file.write("			<YAxis>vddSpec_axis</YAxis>\n")
    file.write("		</Shmoo>\n")
    file.write("		<Shmoo name=\"shmoo2\">\n")
    file.write("			<XAxis>avddSpec_axis</XAxis>\n")
    file.write("		</Shmoo>\n")
    file.write("	</Shmoos>\n")
    file.write("</Blocks>")


def write_runresultmap_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<RunResultMap>\n")
    file.write("		<FlowItemRef name=\"Dctest1_Flow\">\n")
    file.write("			<Result value=\"1\">Fail 1 GHz</Result>\n")
    file.write("			<Result value=\"-1\">All Fail</Result>\n")
    file.write("			<Result value=\"0\">All Pass</Result>\n")
    file.write("			<Default>Uninterpreted Run Result</Default>\n")
    file.write("		</FlowItemRef>\n")
    file.write("	</RunResultMap>\n")
    file.write("</Blocks>")


def write_flows_file(file, unknown_swbin_id):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<Flow name=\"INSTALL_FLOW\">\n")
    file.write("		<FlowItem name=\"START\">\n")
    file.write("			<Type>Entrance</Type>\n")
    file.write("			<Goto result=\"0\">\n")
    file.write("				<FlowItemRef>END</FlowItemRef>\n")
    file.write("				<PassFail>Pass</PassFail>\n")
    file.write("			</Goto>\n")
    file.write("		</FlowItem>\n")
    file.write("		<FlowItem name=\"END\">\n")
    file.write("			<Type>Exit</Type>\n")
    file.write("		</FlowItem>\n")
    file.write("	</Flow>\n")
    file.write("	<Flow name=\"INIT_FLOW\">\n")
    file.write("		<FlowItem name=\"START\">\n")
    file.write("			<Type>Entrance</Type>\n")
    file.write("			<Goto result=\"0\">\n")
    file.write("				<FlowItemRef>END</FlowItemRef>\n")
    file.write("				<PassFail>Pass</PassFail>\n")
    file.write("			</Goto>\n")
    file.write("		</FlowItem>\n")
    file.write("		<FlowItem name=\"END\">\n")
    file.write("			<Type>Exit</Type>\n")
    file.write("		</FlowItem>\n")
    file.write("	</Flow>\n")
    file.write("	<Flow name=\"MAIN_FLOW\">\n")
    file.write("		<FlowItem name=\"START\">\n")
    file.write("			<Type>Entrance</Type>\n")
    file.write("			<Goto result=\"0\">\n")
    file.write("				<SoftBinRef binRef=\"Default\" group=\"SoftBins\">" + str(
        unknown_swbin_id) + "</SoftBinRef>\n")
    file.write("				<FlowItemRef>END</FlowItemRef>\n")
    file.write("				<PassFail>Pass</PassFail>\n")
    file.write("			</Goto>\n")
    file.write("		</FlowItem>\n")
    file.write("		<FlowItem name=\"END\">\n")
    file.write("			<Type>Exit</Type>\n")
    file.write("		</FlowItem>\n")
    file.write("	</Flow>\n")
    file.write("	<Flow name=\"ALARM_FLOW\">\n")
    file.write("		<FlowItem name=\"START\">\n")
    file.write("			<Type>Entrance</Type>\n")
    file.write("			<Goto result=\"0\">\n")
    file.write("				<FlowItemRef>END</FlowItemRef>\n")
    file.write("				<PassFail>Pass</PassFail>\n")
    file.write("			</Goto>\n")
    file.write("		</FlowItem>\n")
    file.write("		<FlowItem name=\"END\">\n")
    file.write("			<Type>Exit</Type>\n")
    file.write("		</FlowItem>\n")
    file.write("	</Flow>\n")
    file.write("	<Flow name=\"POWERDOWN_FLOW\">\n")
    file.write("		<FlowItem name=\"START\">\n")
    file.write("			<Type>Entrance</Type>\n")
    file.write("			<Goto result=\"0\">\n")
    file.write("				<FlowItemRef>END</FlowItemRef>\n")
    file.write("				<PassFail>Pass</PassFail>\n")
    file.write("			</Goto>\n")
    file.write("		</FlowItem>\n")
    file.write("		<FlowItem name=\"END\">\n")
    file.write("			<Type>Exit</Type>\n")
    file.write("		</FlowItem>\n")
    file.write("	</Flow>\n")
    file.write("</Blocks>")


def write_empty_file(file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("</Blocks>")


def generate_project(excel_dir, project_directory):
    dir_list = [project_directory,
                path.join(project_directory, 'XML'),
                path.join(project_directory, 'UserExtension'),
                path.join(project_directory, 'Pattern'),
                path.join(project_directory, 'UserExtension\\x86'),
                path.join(project_directory, 'UserExtension\\x64'),
                path.join(project_directory, 'UserExtension\\x86\debug'),
                path.join(project_directory, 'UserExtension\\x86\\release'),
                path.join(project_directory, 'UserExtension\\x64\debug'),
                path.join(project_directory, 'UserExtension\\x64\\release')
                ]
    for dir in dir_list:
        mkdir(dir)
    source_project_path = path.join(path.dirname(excel_dir), 'Project.xml')
    target_project_path = path.join(project_directory, 'Project.xml')
    bindefinition_path = path.join(project_directory, 'XML\BinDefinition.xml')
    signal_path = path.join(project_directory, 'XML\Signals.xml')
    socketmap_path = path.join(project_directory, 'XML\SocketMap.xml')
    signalgroups_path = path.join(project_directory, 'XML\SignalGroups.xml')
    testblock_path = path.join(project_directory, 'XML\TestBlock.xml')
    limit_path = path.join(project_directory, 'XML\Limit.xml')
    uservars_path = path.join(project_directory, 'XML\\UserVars.xml')
    levels_path = path.join(project_directory, 'XML\Levels.xml')
    specset_path = path.join(project_directory, 'XML\SpecSet.xml')
    timing_path = path.join(project_directory, 'XML\Timing.xml')
    timingmap_path = path.join(project_directory, 'XML\TimingMap.xml')
    patternburst_path = path.join(project_directory, 'XML\PatternBurst.xml')
    shmoo_path = path.join(project_directory, 'XML\Shmoo.xml')
    testerconfig_path = path.join(project_directory, 'XML\TesterConfig.xml')
    testprogram_path = path.join(project_directory, 'XML\TestProgram.xml')
    runresultmap_path = path.join(project_directory, 'XML\RunResultMap.xml')
    source_flows_path = path.join(path.dirname(excel_dir), 'Flows.xml')
    target_flows_path = path.join(project_directory, 'XML\Flows.xml')

    # 数据提取与组装
    pinmap_df = read_excel(excel_dir, sheet_name='PinMap')
    signal_df = pinmap_df.iloc[:35, [5, 6]]

    signals_data = []
    for i in range(signal_df.dropna().shape[0]):
        temp_list = []
        for j in range(signal_df.dropna().shape[1]):
            temp_list.append(signal_df.dropna().iloc[i, j])
        signals_data.append(temp_list)

    channel_id_list = [(0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 'M0', 'M1', 'M2', 'M3', 'M4', 'M5',
                        'M6', 'M7', 2000, 2001, 2002, 2003, 5065, 5068, 5069, 5048, 5049, 5050, 5051),
                       (6, 7, 8, 9, 10, 11, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 'M8', 'M9', 'M10', 'M11', 'M12',
                        'M13', 'M14', 'M15', 2004, 2005, 2006, 2007, 5064, 5070, 5071, 5048, 5049, 5050, 5051)]

    signal_notnull_df = pinmap_df.iloc[:35, 5].notnull()
    segment_df = pinmap_df.iloc[:, 0].dropna()
    socketmap_data = []
    for i in range(signal_notnull_df.shape[0]):
        if signal_notnull_df.iloc[i]:
            temp_list = [signal_df.iloc[i, 0]]
            for j in range(segment_df.shape[0]):
                temp_list.append('0.' + segment_df.iloc[j].split('/')[0][4:].replace('_', '.') + '.' + str(
                    channel_id_list[j % 2][i]))
            socketmap_data.append(temp_list)

    signalgroups_df = read_excel(excel_dir, sheet_name='PinGroup')
    signalgroups_data = []
    for i in range(signalgroups_df.shape[0]):
        temp_list = []
        for j in range(signalgroups_df.shape[1]):
            temp_list.append(signalgroups_df.iloc[i, j])
        signalgroups_data.append(temp_list)

    bindefinition_df = read_excel(excel_dir, sheet_name='BinMap')
    swbin_df = bindefinition_df.iloc[:, :4]
    unknown_row = swbin_df[swbin_df.iloc[:, 1].isin(['Unknown'])]
    unknown_swbin_id = unknown_row.iloc[0, 0]
    hwbin_df = bindefinition_df.iloc[:, 5:9].dropna(axis=0)
    bindefinition_data = []
    swbin_data = []
    hwbin_data = []
    for i in range(swbin_df.shape[0]):
        temp_list = []
        for j in range(swbin_df.shape[1]):
            temp_list.append(swbin_df.iloc[i, j])
        swbin_data.append(temp_list)
    for i in range(hwbin_df.shape[0]):
        temp_list = []
        for j in range(hwbin_df.shape[1]):
            temp_list.append(hwbin_df.iloc[i, j])
        hwbin_data.append(temp_list)
    bindefinition_data.append(swbin_data)
    bindefinition_data.append(hwbin_data)

    speclimits_df = read_excel(excel_dir, sheet_name='SpecLimits')
    limit_df = speclimits_df.iloc[:139, 2:6].dropna()
    limits_df = read_excel(excel_dir, sheet_name='Limits')
    limits_data = []
    for i in range(limit_df.shape[0]):
        temp_list = [i + 1]
        for j in range(limit_df.shape[1]):
            temp_list.append(limit_df.iloc[i, j])
        temp_list += ['', '']
        limits_data.append(temp_list)
    for i in range(limits_df.shape[0]):
        temp_list = []
        for j in range(limits_df.shape[1]):
            data = limits_df.iloc[i, j]
            if isinstance(data, float) and isnan(data):
                data = ''
            temp_list.append(data)
        limits_data.append(temp_list)

    dcmeasure_df = read_excel(excel_dir, sheet_name='DCMeasure').dropna(axis=0, how='all')
    dcmeasure_notnull_df = dcmeasure_df.notnull()
    dcmeasure_data = []
    temp_list1 = []
    for i in range(dcmeasure_df.shape[0]):
        temp_list2 = []
        if dcmeasure_notnull_df.iloc[i, 0]:
            if i > 0:
                dcmeasure_data.append(temp_list1)
                temp_list1 = []
            temp_list1.append(dcmeasure_df.iloc[i, 0])
        for j in range(1, dcmeasure_df.shape[1]):
            temp_list2.append(dcmeasure_df.iloc[i, j])
        temp_list1.append(temp_list2)
    dcmeasure_data.append(temp_list1)

    test_df = read_excel(excel_dir, sheet_name='Test')
    test_notnull_df = test_df.notnull()
    test_data = []
    for i in range(test_df.shape[0]):
        temp_list = []
        for j in range(test_df.shape[1]):
            if j >= 3:
                if test_notnull_df.iloc[i, j]:
                    temp_list.append(test_df.iloc[i, j].split(':')[0])
                    temp_list.append(test_df.iloc[i, j].split(':')[1])
                else:
                    temp_list.append('')
                    temp_list.append('')
            else:
                temp_list.append(test_df.iloc[i, j])
        test_data.append(temp_list)

    block_data = []
    block_data.append(dcmeasure_data)
    block_data.append(test_data)

    uservars_df = read_excel(excel_dir, sheet_name='UserVars')
    uservars_data = []
    for i in range(uservars_df.shape[0]):
        temp_list = []
        for j in range(uservars_df.shape[1]):
            temp_list.append(uservars_df.iloc[i, j])
        uservars_data.append(temp_list)

    levels_df = read_excel(excel_dir, sheet_name='Level')
    levels_notnull_df = levels_df.notnull()
    levels_data = []
    temp_list1 = []
    for i in range(levels_df.shape[0]):
        temp_list2 = []
        if levels_notnull_df.iloc[i, 0]:
            if i > 0:
                levels_data.append(temp_list1)
                temp_list1 = []
            temp_list1.append(levels_df.iloc[i, 0])
        for j in range(1, levels_df.shape[1]):
            data = levels_df.iloc[i, j]
            if isinstance(data, float) and isnan(data):
                data = ''
            temp_list2.append(data)
        temp_list1.append(temp_list2)
    levels_data.append(temp_list1)

    if path.exists(source_project_path):
        copy(source_project_path, target_project_path)
        DOMTree = parse(source_project_path)
        collection = DOMTree.documentElement
        socketmap_name = collection.getElementsByTagName("Project")[0].getElementsByTagName("SocketMap")[0].getElementsByTagName(
            "Ref")[0].childNodes[0].data
    else:
        with open(target_project_path, 'w') as project_file:
            write_project_file(project_file)
        socketmap_name = 'SocketMap'
    with open(signal_path, 'w') as signal_file:
        write_signals_file(signals_data, signal_file)
    with open(socketmap_path, 'w') as socketmap_file:
        write_socketmap_file(socketmap_data, socketmap_file, socketmap_name)
    with open(signalgroups_path, 'w') as signalgroups_file:
        write_signalgroups_file(signalgroups_data, signalgroups_file)
    with open(bindefinition_path, 'w') as bindefinition_file:
        write_bindefinition_file(bindefinition_data, bindefinition_file)
    with open(limit_path, 'w') as limit_file:
        write_limit_file(limits_data, limit_file)
    with open(testblock_path, 'w') as testblock_file:
        write_block_file(block_data, testblock_file, socketmap_name)
    with open(uservars_path, 'w') as uservars_file:
        write_uservars_file(uservars_data, uservars_file)
    with open(levels_path, 'w') as levels_file:
        write_levels_file(levels_data, levels_file)
    with open(testerconfig_path, 'w') as testerconfig_file:
        write_config_file(testerconfig_file)
    with open(testprogram_path, 'w') as testprogram_file:
        write_program_file(testprogram_file)
    with open(shmoo_path, 'w') as shmoo_file:
        write_shmoo_file(shmoo_file)
    with open(runresultmap_path, 'w') as runresultmap_file:
        write_runresultmap_file(runresultmap_file)
    with open(specset_path, 'w') as specset_file:
        write_empty_file(specset_file)
    with open(timing_path, 'w') as timing_file:
        write_empty_file(timing_file)
    with open(timingmap_path, 'w') as timingmap_file:
        write_empty_file(timingmap_file)
    with open(patternburst_path, 'w') as patternburst_file:
        write_empty_file(patternburst_file)
    if path.exists(source_flows_path):
        copy(source_flows_path, target_flows_path)
    else:
        with open(target_flows_path, 'w') as flows_file:
            write_flows_file(flows_file, unknown_swbin_id)


def main():
    # Project文件夹路径
    if argv.count('-d') == 0:
        print("Error：Project文件夹路径必填，格式：“-d D:\F28_Dual_DVP”。")
        exit()
    else:
        project_directory = argv[argv.index('-d') + 1]
        if project_directory[:2] == '.\\':
            project_directory = getcwd() + project_directory[1:]

    # Excel文件路径
    if argv.count('-f') == 0:
        print("Error：Excel文件路径必填，格式：“-f D:\Example_v2.0.xlsx”。")
        exit()
    else:
        excel_dir = argv[argv.index('-f') + 1]

    # 生成文件
    generate_project(excel_dir, project_directory)


if __name__ == "__main__":
    main()
    exit()
