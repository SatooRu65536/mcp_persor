import pandas as pd
import numpy as np
import re


class BVHparser:
    def __init__(self, filename):
        self.bvh = self.__readFile(filename)

        lines = self.bvh.split('\n')

        hierarchy_tokens = self.__getHierarchyTokens(lines)
        self.skeleton = self.__getJointData(hierarchy_tokens)

        (frame_time, frames, motion) = self.__getMotionData(lines)

        self.frame_time = frame_time
        self.frames = frames
        self.motion = motion

    def __readFile(self, filename):
        '''
        BVHファイルを読み込む

        Parameters
        ----------
        filename : str
            BVHファイルのパス
        '''

        with open(filename, 'r') as f:
            return f.read()

    def __getMotion(self):
        '''
        BVHファイルからモーションデータを取得する

        Returns
        -------
        list
            モーションデータ
        '''

        motion = self.bvh.split('Frame Time:')[1]
        motion = motion.split("\n")
        return motion[1:]

    def __try_to_float(self, s):
        '''
        文字列をfloatに変換する

        Parameters
        ----------
        s : str
            変換する文字列

        Returns
        -------
        float
            変換後の値
        '''

        try:
            return float(s)
        except ValueError:
            return None

    def __getHierarchyTokens(self, lines):
        '''
        BVHファイルからHierarchy部をトークンごとの配列に変換する

        Parameters
        ----------
        lines : list
            BVHファイルの行データ

        Returns
        -------
        list
            階層構造のトークン
        '''

        tokens = []
        index = 0
        nesting_level = 0
        is_closeing = False

        for i in range(len(lines)):
            line = lines.pop(0)
            tokens += line.split()
            nesting_level += line.count('{') - line.count('}')
            index += 1
            if line.count('}') > 0:
                is_closeing = True
            if nesting_level == 0 and is_closeing:
                break

        return tokens

    def __getJointData(self, tokens):
        '''
        トークン配列からJointデータを取得する

        Parameters
        ----------
        tokens : list
            Hierarchy部のトークン

        Returns
        -------
        dict
            Jointデータ
        '''

        skeleton = {}
        joint_name = None
        joint_list = []

        for i in range(len(tokens)):
            if tokens[i] == '{':
                joint_list.append(joint_name)
            elif tokens[i] == '}':
                joint_list.pop()

            if tokens[i] == 'ROOT':
                joint_name = tokens[i+1]
                skeleton[tokens[i+1]] = {
                    'joint': None,
                    'offset': [],
                    'channels': [],
                }
            elif tokens[i] == 'JOINT':
                joint_name = tokens[i+1]
                skeleton[tokens[i+1]] = {
                    'joint': joint_list[-1],
                    'offset': [],
                    'channels': [],
                }
            elif tokens[i] == 'OFFSET':
                index = i + 1
                while self.__try_to_float(tokens[index]) != None:
                    offset = self.__try_to_float(tokens[index])
                    skeleton[joint_name]['offset'].append(offset)
                    index += 1
                i = index - 1
            elif tokens[i] == 'CHANNELS':
                index = i + 2
                while tokens[index] not in ['OFFSET', 'CHANNELS', 'JOINT', '{']:
                    skeleton[joint_name]['channels'].append(tokens[index])
                    index += 1
                i = index - 1

        return skeleton

    def __getMotionData(self, lines):
        '''
        トークン配列からモーションデータを取得する

        Parameters
        ----------
        tokens : list
            Motion部のトークン

        Returns
        -------
        list
            モーションデータ
        '''

        motion = []
        frames = None
        frame_time = None
        for i in range(len(lines)):
            if 'Frames:' in lines[i]:
                frame_time = self.__try_to_float(lines[i].split()[1])
            elif 'Frame Time:' in lines[i]:
                frames = self.__try_to_float(lines[i].split()[2])
            else:
                motion += [self.__try_to_float(v) for v in lines[i].split()]

        return (frame_time, frames, motion)

    def getSkeletonPathToRoot(self, joint):
        '''
        指定したjointからrootまでのパスを取得する

        Parameters
        ----------
        joint : str
            パスを取得するjoint

        Returns
        -------
        list
            jointからrootまでのパス
        '''

        path = []
        while joint != None:
            path.append(joint)
            joint = self.skeleton[joint]['joint']

        return path

    def getMotionDataframe(self):
        '''
        BVHファイルからモーションデータを取得する

        Returns
        -------
        pandas.DataFrame
            モーションデータ
        '''

        motion = [m.rstrip().split(' ') for m in self.__getMotion() if m != '']

        motion_df = pd.DataFrame(motion)
        motion_df.columns = [
            'root_Xposition', 'root_Yposition', 'root_Zposition', 'root_Xrotation', 'root_Yrotation', 'root_Zrotation',
            'torso_1_Xposition', 'torso_1_Yposition', 'torso_1_Zposition', 'torso_1_Xrotation', 'torso_1_Yrotation', 'torso_1_Zrotation',
            'torso_2_Xposition', 'torso_2_Yposition', 'torso_2_Zposition', 'torso_2_Xrotation', 'torso_2_Yrotation', 'torso_2_Zrotation',
            'torso_3_Xposition', 'torso_3_Yposition', 'torso_3_Zposition', 'torso_3_Xrotation', 'torso_3_Yrotation', 'torso_3_Zrotation',
            'torso_4_Xposition', 'torso_4_Yposition', 'torso_4_Zposition', 'torso_4_Xrotation', 'torso_4_Yrotation', 'torso_4_Zrotation',
            'torso_5_Xposition', 'torso_5_Yposition', 'torso_5_Zposition', 'torso_5_Xrotation', 'torso_5_Yrotation', 'torso_5_Zrotation',
            'torso_6_Xposition', 'torso_6_Yposition', 'torso_6_Zposition', 'torso_6_Xrotation', 'torso_6_Yrotation', 'torso_6_Zrotation',
            'torso_7_Xposition', 'torso_7_Yposition', 'torso_7_Zposition', 'torso_7_Xrotation', 'torso_7_Yrotation', 'torso_7_Zrotation',
            'neck_1_Xposition', 'neck_1_Yposition', 'neck_1_Zposition', 'neck_1_Xrotation', 'neck_1_Yrotation', 'neck_1_Zrotation',
            'neck_2_Xposition', 'neck_2_Yposition', 'neck_2_Zposition', 'neck_2_Xrotation', 'neck_2_Yrotation', 'neck_2_Zrotation',
            'head_Xposition', 'head_Yposition', 'head_Zposition', 'head_Xrotation', 'head_Yrotation', 'head_Zrotation',
            'l_shoulder_Xposition', 'l_shoulder_Yposition', 'l_shoulder_Zposition', 'l_shoulder_Xrotation', 'l_shoulder_Yrotation', 'l_shoulder_Zrotation',
            'l_up_arm_Xposition', 'l_up_arm_Yposition', 'l_up_arm_Zposition', 'l_up_arm_Xrotation', 'l_up_arm_Yrotation', 'l_up_arm_Zrotation',
            'l_low_arm_Xposition', 'l_low_arm_Yposition', 'l_low_arm_Zposition', 'l_low_arm_Xrotation', 'l_low_arm_Yrotation', 'l_low_arm_Zrotation',
            'l_hand_Xposition', 'l_hand_Yposition', 'l_hand_Zposition', 'l_hand_Xrotation', 'l_hand_Yrotation', 'l_hand_Zrotation',
            'r_shoulder_Xposition', 'r_shoulder_Yposition', 'r_shoulder_Zposition', 'r_shoulder_Xrotation', 'r_shoulder_Yrotation', 'r_shoulder_Zrotation',
            'r_up_arm_Xposition', 'r_up_arm_Yposition', 'r_up_arm_Zposition', 'r_up_arm_Xrotation', 'r_up_arm_Yrotation', 'r_up_arm_Zrotation',
            'r_low_arm_Xposition', 'r_low_arm_Yposition', 'r_low_arm_Zposition', 'r_low_arm_Xrotation', 'r_low_arm_Yrotation', 'r_low_arm_Zrotation',
            'r_hand_Xposition', 'r_hand_Yposition', 'r_hand_Zposition', 'r_hand_Xrotation', 'r_hand_Yrotation', 'r_hand_Zrotation',
            'l_up_leg_Xposition', 'l_up_leg_Yposition', 'l_up_leg_Zposition', 'l_up_leg_Xrotation', 'l_up_leg_Yrotation', 'l_up_leg_Zrotation',
            'l_low_leg_Xposition', 'l_low_leg_Yposition', 'l_low_leg_Zposition', 'l_low_leg_Xrotation', 'l_low_leg_Yrotation', 'l_low_leg_Zrotation',
            'l_foot_Xposition', 'l_foot_Yposition', 'l_foot_Zposition', 'l_foot_Xrotation', 'l_foot_Yrotation', 'l_foot_Zrotation',
            'l_toes_Xposition', 'l_toes_Yposition', 'l_toes_Zposition', 'l_toes_Xrotation', 'l_toes_Yrotation', 'l_toes_Zrotation',
            'r_up_leg_Xposition', 'r_up_leg_Yposition', 'r_up_leg_Zposition', 'r_up_leg_Xrotation', 'r_up_leg_Yrotation', 'r_up_leg_Zrotation',
            'r_low_leg_Xposition', 'r_low_leg_Yposition', 'r_low_leg_Zposition', 'r_low_leg_Xrotation', 'r_low_leg_Yrotation', 'r_low_leg_Zrotation',
            'r_foot_Xposition', 'r_foot_Yposition', 'r_foot_Zposition', 'r_foot_Xrotation', 'r_foot_Yrotation', 'r_foot_Zrotation',
            'r_toes_Xposition', 'r_toes_Yposition', 'r_toes_Zposition', 'r_toes_Xrotation', 'r_toes_Yrotation', 'r_toes_Zrotation',
        ]
        time = np.arange(0, motion_df.shape[0]) * self.frame_time
        motion_df.insert(0, 'time', time)
        for column in motion_df.columns:
            motion_df[column] = pd.to_numeric(
                motion_df[column], errors='coerce')
        return motion_df

    def getRelativeMotionDataframe(self, joint):
        '''
        BVHファイルからモーションデータを取得する

        Returns
        -------
        pandas.DataFrame
            モーションデータ
        '''

        joint_motion_df = self.getMotionDataframe()[[
            'time',
            f'{joint}_Xposition',
            f'{joint}_Yposition',
            f'{joint}_Zposition',
            f'{joint}_Xrotation',
            f'{joint}_Yrotation',
            f'{joint}_Zrotation',
        ]]

        # カラム名から {joint}_ を削除
        columns = joint_motion_df.columns
        joint_motion_df.columns = [c.replace(f'{joint}_', '') for c in columns]

        return joint_motion_df

    def getAbsoluteMotionDataframe(self, joint):
        '''
        BVHファイルからモーションデータを取得する

        Returns
        -------
        pandas.DataFrame
            モーションデータ
        '''

        motion_df = self.getMotionDataframe()
        path = self.getSkeletonPathToRoot(joint)

        for i in range(1, len(path)):
            motion_df[f'{joint}_Xposition'] += motion_df[f'{path[i]}_Xposition']
            motion_df[f'{joint}_Yposition'] += motion_df[f'{path[i]}_Yposition']
            motion_df[f'{joint}_Zposition'] += motion_df[f'{path[i]}_Zposition']

        # motion_df から time と joint 始まりの列を残す
        columns = motion_df.columns
        columns = [c for c in columns if c.startswith(joint) or c == 'time']
        joint_motion_df = motion_df[columns]

        # カラム名から {joint}_ を削除
        joint_motion_df.columns = [c.replace(f'{joint}_', '') for c in columns]

        return joint_motion_df

    def getJoints(self):
        '''
        関節名のリストを取得する

        Returns
        -------
        list
            関節名のリスト
        '''

        return self.skeleton.keys()
