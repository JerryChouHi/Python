# encoding:utf-8
# @Time     : 2019/8/9 9:37
# @Author   : Jerry Chou
# @File     : Excel_to_Xml.py
# @Function :

from sys import argv, exit
from os import getcwd, makedirs
from os.path import join, dirname, exists
from xml.dom.minidom import parse
from shutil import copy
from xlrd import open_workbook
from datetime import datetime


def mkdir(path):
    """
    创建文件夹目录
    :param path: 文件夹目录
    :return:
    """
    path = path.strip()
    path = path.rstrip("\\")
    is_exists = exists(path)
    if not is_exists:
        makedirs(path)
        return True
    else:
        return False


def data_convert(data):
    """
    如果是浮点数，去掉小数点后末尾的0；
    如果是字符串，去掉头尾空格
    :param data: 
    :return: 
    """
    if isinstance(data, float):
        return '{:g}'.format(data)
    else:
        return data.strip()


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
        file.write("			<Bin name=\"" + data[1][i][1] + "\">\n")
        file.write("				<ID>" + data[1][i][0] + "</ID>\n")
        file.write("				<Desc>" + data[1][i][3] + "</Desc>\n")
        file.write("				<Inherit>" + data[1][i][2] + "</Inherit>\n")
        file.write("			</Bin>\n")
    file.write("		</BinGroup>\n")
    file.write("		<BinGroup name=\"SoftBins\" type=\"SoftBin\">\n")
    for i in range(len(data[0])):
        file.write("			<Bin name=\"" + data[0][i][1] + "\">\n")
        file.write("				<ID>" + data[0][i][0] + "</ID>\n")
        file.write("				<Desc>" + data[0][i][2] + "</Desc>\n")
        for j in range(len(data[1])):
            if data[1][j][0] == data[0][i][3]:
                file.write("				<Inherit>" + data[1][j][1] + "</Inherit>\n")
        file.write("			</Bin>\n")
    file.write("		</BinGroup>\n")
    file.write("	</BinDefs>\n")
    file.write("</Blocks>")


def write_limit_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    for i in range(len(data)):
        file.write("	<Limit name=\"" + data[i][0] + "\">\n")
        file.write("		<TestNum>" + str(i + 1) + "</TestNum>\n")
        if data[i][2] != '':
            file.write("		<LoLimit>" + data[i][2] + "</LoLimit>\n")
        if data[i][1] != '':
            file.write("		<HiLimit>" + data[i][1] + "</HiLimit>\n")
        if data[i][3] != '':
            file.write("		<Unit>" + data[i][3] + "</Unit>\n")
        if data[i][4] != '':
            file.write(
                "		<SoftBinRef binRef=\"Default\" group=\"SoftBins\">" + data[i][4] + "</SoftBinRef>\n")
        if data[i][5] != '':
            file.write("		<Description>" + data[i][5] + "</Description>\n")
        file.write("	</Limit>\n")
    file.write("</Blocks>")


def write_block_file(data, file):
    file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file.write("<Blocks>\n")
    file.write("	<DCMeasures>\n")
    for i in range(len(data[0])):
        file.write("		<DCMeasure name=\"" + data[0][i][0] + "\">\n")
        for j in range(1, len(data[0][i])):
            file.write("			<MeasureGroup sigRef=\"" + data[0][i][j][0] + "\" minorTestNum=\"" +
                       data[0][i][j][1] + "\">\n")
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
                file.write("				<SampleNum>" + data[0][i][j][10] + "</SampleNum>\n")
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
    for i in range(len(data[1])):
        file.write("		<TestCondition name=\"" + data[1][i][0] + "\"/>\n")
    file.write("	</TestConditions>\n")
    file.write("	<Tests>\n")
    for i in range(len(data[1])):
        file.write("		<Test name=\"" + data[1][i][0] + "\" testNum=\"" + data[1][i][1] + "\">\n")
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
                file.write("			<VPS>" + data[i][j][1] + "</VPS>\n")
            if data[i][j][2] != '':
                file.write("			<IClamp>" + data[i][j][2] + "</IClamp>\n")
            if data[i][j][3] != '':
                file.write("			<IRange>" + data[i][j][3] + "</IRange>\n")
            if data[i][j][4] != '':
                file.write("			<Delay>" + data[i][j][4] + "</Delay>\n")
            if data[i][j][5] != '':
                file.write("			<VIL>" + data[i][j][5] + "</VIL>\n")
            if data[i][j][6] != '':
                file.write("			<VIH>" + data[i][j][6] + "</VIH>\n")
            if data[i][j][7] != '':
                file.write("			<VTERM>" + data[i][j][7] + "</VTERM>\n")
            if data[i][j][8] != '':
                file.write("			<VTERM_EN>" + data[i][j][8] + "</VTERM_EN>\n")
            if data[i][j][9] != '':
                file.write("			<VOL>" + data[i][j][9] + "</VOL>\n")
            if data[i][j][10] != '':
                file.write("			<VOH>" + data[i][j][10] + "</VOH>\n")
            if data[i][j][11] != '':
                file.write("			<VCH>" + data[i][j][11] + "</VCH>\n")
            if data[i][j][12] != '':
                file.write("			<VCL>" + data[i][j][12] + "</VCL>\n")
            file.write("		</SigRef>\n")
        file.write("	</Levels>\n")
    file.write("</Blocks>")


def write_project_file(data, file):
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
    file.write("			<Ref>" + data[0] + "</Ref>\n")
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
    if len(data[1]) > 0:
        for i in range(len(data[1])):
            file.write("		<" + data[1][i][0] + ">" + data[1][i][1] + "</" + data[1][i][0] + ">\n")
    file.write("		<SeparateLog>\n")
    file.write("			<Enable>true</Enable>\n")
    file.write("			<Manual>Manual_%s</Manual>\n")
    file.write("			<Lot>Lot_%s</Lot>\n")
    file.write("		</SeparateLog>\n")
    file.write("	</Datalog>\n")
    if len(data[2]) > 0:
        file.write("	<ProjectSetup>\n")
        for i in range(len(data[2])):
            file.write("		<" + data[2][i][0] + ">" + data[2][i][1] + "</" + data[2][i][0] + ">\n")
        file.write("	</ProjectSetup>\n")
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
    file.write("				<SoftBinRef binRef=\"Default\" group=\"SoftBins\">" +
               unknown_swbin_id + "</SoftBinRef>\n")
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
    directory_list = [project_directory,
                      join(project_directory, 'XML'),
                      join(project_directory, 'UserExtension'),
                      join(project_directory, 'Pattern'),
                      join(project_directory, 'UserExtension\\x86'),
                      join(project_directory, 'UserExtension\\x64'),
                      join(project_directory, 'UserExtension\\x86\debug'),
                      join(project_directory, 'UserExtension\\x86\\release'),
                      join(project_directory, 'UserExtension\\x64\debug'),
                      join(project_directory, 'UserExtension\\x64\\release')
                      ]
    source_project_path = join(dirname(excel_dir), 'Project.xml')
    target_project_path = join(project_directory, 'Project.xml')
    bindefinition_path = join(project_directory, 'XML\BinDefinition.xml')
    signal_path = join(project_directory, 'XML\Signals.xml')
    socketmap_path = join(project_directory, 'XML\SocketMap.xml')
    signalgroups_path = join(project_directory, 'XML\SignalGroups.xml')
    testblock_path = join(project_directory, 'XML\TestBlock.xml')
    limit_path = join(project_directory, 'XML\Limit.xml')
    uservars_path = join(project_directory, 'XML\\UserVars.xml')
    levels_path = join(project_directory, 'XML\Levels.xml')
    specset_path = join(project_directory, 'XML\SpecSet.xml')
    timing_path = join(project_directory, 'XML\Timing.xml')
    timingmap_path = join(project_directory, 'XML\TimingMap.xml')
    patternburst_path = join(project_directory, 'XML\PatternBurst.xml')
    shmoo_path = join(project_directory, 'XML\Shmoo.xml')
    testerconfig_path = join(project_directory, 'XML\TesterConfig.xml')
    testprogram_path = join(project_directory, 'XML\TestProgram.xml')
    runresultmap_path = join(project_directory, 'XML\RunResultMap.xml')
    source_flows_path = join(dirname(excel_dir), 'Flows.xml')
    target_flows_path = join(project_directory, 'XML\Flows.xml')

    # 数据提取与组装
    excel_data = open_workbook(excel_dir)
    project_sheet = excel_data.sheet_by_name('Project')
    project_data = [project_sheet.cell_value(0, 2)]
    datalog_row = -1
    projectsetup_row = -1
    for i in range(1, project_sheet.nrows):
        if project_sheet.cell_value(i, 0) == 'Datalog':
            datalog_row = i
        if project_sheet.cell_value(i, 0) == 'ProjectSetup':
            projectsetup_row = i
    if datalog_row != -1:
        temp_list = []
        if projectsetup_row == -1:
            for i in range(datalog_row, project_sheet.nrows):
                if len(str(project_sheet.cell_value(i, 2))) > 0:
                    temp_list.append((project_sheet.cell_value(i, 1), data_convert(project_sheet.cell_value(i, 2))))
        else:
            for i in range(datalog_row, projectsetup_row):
                if len(str(project_sheet.cell_value(i, 2))) > 0:
                    temp_list.append((project_sheet.cell_value(i, 1), data_convert(project_sheet.cell_value(i, 2))))
        project_data.append(temp_list)
    if projectsetup_row != -1:
        temp_list = []
        for i in range(projectsetup_row, project_sheet.nrows):
            if len(project_sheet.cell_value(i, 2)) > 0:
                temp_list.append((project_sheet.cell_value(i, 1), data_convert(project_sheet.cell_value(i, 2))))
        project_data.append(temp_list)

    channel_id_list = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        'M0',
        'M1',
        'M2',
        'M3',
        'M4',
        'M5',
        'M6',
        'M7',
        'M8',
        'M9',
        'M10',
        'M11',
        'M12',
        'M13',
        'M14',
        'M15',
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        5048,
        5049,
        5050,
        5051,
        5052,
        5053,
        5054,
        5055,
        5056,
        5057,
        5058,
        5059,
        5060,
        5061,
        5062,
        5063,
        5064,
        5065,
        5066,
        5067,
        5068,
        5069,
        5070,
        5071,
        5072,
        5073,
        5074,
        5075
    ]
    segment_pin_num = len(channel_id_list)
    pinmap_sheet = excel_data.sheet_by_name('PinMap')
    signals_data = []
    for row_num in range(1, segment_pin_num + 1):
        if len(pinmap_sheet.cell_value(row_num, 5)) > 0:
            signals_data.append(
                (data_convert(pinmap_sheet.cell_value(row_num, 5)), data_convert(pinmap_sheet.cell_value(row_num, 6))))

    segment_list = []
    for row_num in range(1, pinmap_sheet.nrows):
        if len(pinmap_sheet.cell_value(row_num, 0)) > 0:
            segment_list.append(data_convert(pinmap_sheet.cell_value(row_num, 0)))
    pin_name_list = []
    start_num = 1
    for i in range(len(segment_list)):
        temp_list = []
        for j in range(start_num, start_num + segment_pin_num):
            temp_list.append(data_convert(pinmap_sheet.cell_value(j, 5)))
        pin_name_list.append(temp_list)
        start_num += (segment_pin_num + 1)
    socketmap_data = []
    for i in range(len(pin_name_list[0])):
        if len(pin_name_list[0][i]) > 0:
            temp_list = []
            pin_name = pin_name_list[0][i]
            temp_list.append(pin_name)
            chassis_id = '0'
            slot_segment_id = segment_list[0].split('/')[0][4:].replace('_', '.')
            channel_id = str(channel_id_list[i])
            temp_list.append(chassis_id + '.' + slot_segment_id + '.' + channel_id)
            for m in range(1, len(pin_name_list)):
                for n in range(len(pin_name_list[m])):
                    if len(pin_name_list[m][n]) > 0:
                        compare_pin_name = pin_name_list[m][n]
                        if pin_name == compare_pin_name:
                            compared_slot_segment_id = segment_list[m].split('/')[0][4:].replace('_', '.')
                            compared_channel_id = str(channel_id_list[n])
                            temp_list.append(chassis_id + '.' + compared_slot_segment_id + '.' + compared_channel_id)
                            break
            socketmap_data.append(temp_list)

    signalgroups_sheet = excel_data.sheet_by_name('PinGroup')
    signalgroups_data = []
    for row_num in range(1, signalgroups_sheet.nrows):
        temp_list = []
        for col_num in range(signalgroups_sheet.ncols):
            temp_list.append(data_convert(signalgroups_sheet.cell_value(row_num, col_num)))
        signalgroups_data.append(temp_list)

    bindefinition_sheet = excel_data.sheet_by_name('BinMap')
    swbin_data = []
    hwbin_data = []
    find_unknown_bin = False
    for row_num in range(1, bindefinition_sheet.nrows):
        if bindefinition_sheet.cell_value(row_num, 1) in ('Unknown', 'Unknow'):
            unknown_swbin_id = data_convert(bindefinition_sheet.cell_value(row_num, 0))
            find_unknown_bin = True
        temp_swbin_list = []
        temp_hwbin_list = []
        for col_num in range(4):
            temp_swbin_list.append(data_convert(bindefinition_sheet.cell_value(row_num, col_num)))
        if len(str(bindefinition_sheet.cell_value(row_num, 5))) > 0:
            for m in range(5, 9):
                temp_hwbin_list.append(data_convert(bindefinition_sheet.cell_value(row_num, m)))
            hwbin_data.append(temp_hwbin_list)
        swbin_data.append(temp_swbin_list)
    if not find_unknown_bin:
        with open(join(project_directory, 'error.log'), 'a', encoding='utf-8-sig') as error_file:
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            error_file.write(time + " Error：BinMap中不存在SWBinName为'Unknown'或'Unknow'，请核查！\n")
        exit()
    bindefinition_data = [swbin_data, hwbin_data]

    limits_sheet = excel_data.sheet_by_name('Limits')
    limits_data = []
    for col_num in range(8, pinmap_sheet.ncols):
        if len(pinmap_sheet.cell_value(0, col_num)) > 0:
            for row_num in range(1, segment_pin_num + 1):
                if len(pinmap_sheet.cell_value(row_num, col_num)) > 0:
                    limit_name = pinmap_sheet.cell_value(row_num, 5) + '_' + pinmap_sheet.cell_value(0, col_num)
                    high_limit = data_convert(pinmap_sheet.cell_value(row_num, col_num))
                    low_limit = data_convert(pinmap_sheet.cell_value(row_num, col_num + 1))
                    unit = data_convert(pinmap_sheet.cell_value(row_num, col_num + 2))
                    limits_data.append([limit_name, high_limit, low_limit, unit, '', ''])

    for row_num in range(1, limits_sheet.nrows):
        temp_list = []
        for col_num in range(limits_sheet.ncols):
            temp_list.append(data_convert(limits_sheet.cell_value(row_num, col_num)))
        limits_data.append(temp_list)

    dcmeasure_sheet = excel_data.sheet_by_name('DCMeasure')
    dcmeasure_data = []
    temp_list1 = []
    for row_num in range(1, dcmeasure_sheet.nrows):
        temp_list2 = []
        if len(dcmeasure_sheet.cell_value(row_num, 0)) > 0:
            if row_num > 1:
                dcmeasure_data.append(temp_list1)
                temp_list1 = []
            temp_list1.append(data_convert(dcmeasure_sheet.cell_value(row_num, 0)))
        if len(dcmeasure_sheet.cell_value(row_num, 1)) > 0:
            for col_num in range(1, dcmeasure_sheet.ncols):
                temp_list2.append(data_convert(dcmeasure_sheet.cell_value(row_num, col_num)))
            temp_list1.append(temp_list2)
    dcmeasure_data.append(temp_list1)

    test_sheet = excel_data.sheet_by_name('Test')
    test_data = []
    for row_num in range(1, test_sheet.nrows):
        temp_list = []
        for col_num in range(test_sheet.ncols):
            if col_num >= 3:
                if len(test_sheet.cell_value(row_num, col_num)) > 0:
                    temp_list.append(test_sheet.cell_value(row_num, col_num).split(':')[0])
                    temp_list.append(test_sheet.cell_value(row_num, col_num).split(':')[1])
                else:
                    temp_list.append('')
                    temp_list.append('')
            else:
                temp_list.append(data_convert(test_sheet.cell_value(row_num, col_num)))
        test_data.append(temp_list)

    block_data = [dcmeasure_data, test_data]

    uservars_sheet = excel_data.sheet_by_name('UserVars')
    uservars_data = []
    for row_num in range(1, uservars_sheet.nrows):
        temp_list = []
        for col_num in range(uservars_sheet.ncols):
            temp_list.append(data_convert(uservars_sheet.cell_value(row_num, col_num)))
        uservars_data.append(temp_list)

    levels_sheet = excel_data.sheet_by_name('Level')
    levels_data = []
    temp_list1 = []
    for row_num in range(1, levels_sheet.nrows):
        temp_list2 = []
        if len(levels_sheet.cell_value(row_num, 0)) > 0:
            if row_num > 1:
                levels_data.append(temp_list1)
                temp_list1 = []
            temp_list1.append(data_convert(levels_sheet.cell_value(row_num, 0)))
        if len(levels_sheet.cell_value(row_num, 1)) > 0:
            for col_num in range(1, levels_sheet.ncols):
                temp_list2.append(data_convert(levels_sheet.cell_value(row_num, col_num)))
            temp_list1.append(temp_list2)
    levels_data.append(temp_list1)

    for directory in directory_list:
        mkdir(directory)
    if exists(source_project_path):
        copy(source_project_path, target_project_path)
        DOMTree = parse(source_project_path)
        collection = DOMTree.documentElement
        socketmap_name = \
            collection.getElementsByTagName("Project")[0].getElementsByTagName("SocketMap")[0].getElementsByTagName(
                "Ref")[0].childNodes[0].data
    else:
        with open(target_project_path, 'w', encoding='utf-8-sig') as project_file:
            write_project_file(project_data, project_file)
        socketmap_name = project_data[0]
    with open(signal_path, 'w', encoding='utf-8-sig') as signal_file:
        write_signals_file(signals_data, signal_file)
    with open(socketmap_path, 'w', encoding='utf-8-sig') as socketmap_file:
        write_socketmap_file(socketmap_data, socketmap_file, socketmap_name)
    with open(signalgroups_path, 'w', encoding='utf-8-sig') as signalgroups_file:
        write_signalgroups_file(signalgroups_data, signalgroups_file)
    with open(bindefinition_path, 'w', encoding='utf-8-sig') as bindefinition_file:
        write_bindefinition_file(bindefinition_data, bindefinition_file)
    with open(limit_path, 'w', encoding='utf-8-sig') as limit_file:
        write_limit_file(limits_data, limit_file)
    with open(testblock_path, 'w', encoding='utf-8-sig') as testblock_file:
        write_block_file(block_data, testblock_file)
    with open(uservars_path, 'w', encoding='utf-8-sig') as uservars_file:
        write_uservars_file(uservars_data, uservars_file)
    with open(levels_path, 'w', encoding='utf-8-sig') as levels_file:
        write_levels_file(levels_data, levels_file)
    with open(testerconfig_path, 'w', encoding='utf-8-sig') as testerconfig_file:
        write_config_file(testerconfig_file)
    with open(testprogram_path, 'w', encoding='utf-8-sig') as testprogram_file:
        write_program_file(testprogram_file)
    with open(shmoo_path, 'w', encoding='utf-8-sig') as shmoo_file:
        write_shmoo_file(shmoo_file)
    with open(runresultmap_path, 'w', encoding='utf-8-sig') as runresultmap_file:
        write_runresultmap_file(runresultmap_file)
    with open(specset_path, 'w', encoding='utf-8-sig') as specset_file:
        write_empty_file(specset_file)
    with open(timing_path, 'w', encoding='utf-8-sig') as timing_file:
        write_empty_file(timing_file)
    with open(timingmap_path, 'w', encoding='utf-8-sig') as timingmap_file:
        write_empty_file(timingmap_file)
    with open(patternburst_path, 'w', encoding='utf-8-sig') as patternburst_file:
        write_empty_file(patternburst_file)
    if exists(source_flows_path):
        copy(source_flows_path, target_flows_path)
    else:
        with open(target_flows_path, 'w', encoding='utf-8-sig') as flows_file:
            write_flows_file(flows_file, unknown_swbin_id)


def main():
    # Project文件夹路径
    if argv.count('-d') == 0:
        print("Error：Project文件夹路径必填，格式：“-d D:\F28_Dual_DVP”。")
        exit()
    else:
        project_directory = argv[argv.index('-d') + 1]
        for i in range(argv.index('-d') + 2, len(argv)):
            if not argv[i].startswith('-'):
                project_directory += (' ' + argv[i])
            else:
                break
        if project_directory[:2] == '.\\':
            project_directory = getcwd() + project_directory[1:]

    # Excel文件路径
    if argv.count('-f') == 0:
        print("Error：Excel文件路径必填，格式：“-f D:\Example_v2.0.xlsx”。")
        exit()
    else:
        excel_dir = argv[argv.index('-f') + 1]
        for i in range(argv.index('-f') + 2, len(argv)):
            if not argv[i].startswith('-'):
                excel_dir += (' ' + argv[i])
            else:
                break

    # 生成文件
    generate_project(excel_dir, project_directory)


if __name__ == "__main__":
    main()
