import pandas as pd
import numpy as np
import re


class BVHparser:
    def __init__(self, filename):
        self.bvh = self.__readFile(filename)

        lines = self.bvh.split('\n')

        hierarchy_tokens = self.__getHierarchyTokens(lines)
        (skeleton, root) = self.__getJointData(hierarchy_tokens)
        self.skeleton = skeleton
        self.root = root
        self.channels = self.__getChannels()

        (frame_time, frames, motion) = self.__getMotionData(lines)

        self.frame_time = frame_time
        self.frames = frames
        self.default_motion_df = self.__getDefaultMotionDataframe(motion)
        self.motion_df = self.default_motion_df.copy()

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
        root = None
        joint_list = []

        reserved_words = ['OFFSET', 'CHANNELS', 'JOINT', '{', 'End']
        for i in range(len(tokens)):
            if tokens[i] == '{':
                joint_list.append(joint_name)
            elif tokens[i] == '}':
                joint_list.pop()

            if tokens[i] == 'ROOT':
                root = tokens[i+1]
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
                while tokens[index] not in reserved_words:
                    skeleton[joint_name]['channels'].append(tokens[index])
                    index += 1
                i = index - 1

        return (skeleton, root)

    def __getChannels(self):
        channels = []
        for j in self.skeleton.keys():
            channels += [f'{j}_{c}' for c in self.skeleton[j]['channels']]

        return channels

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
            if 'MOTION' in lines[i]:
                continue
            elif 'Frames:' in lines[i]:
                frame_time = self.__try_to_float(lines[i].split()[1])
            elif 'Frame Time:' in lines[i]:
                frames = self.__try_to_float(lines[i].split()[2])
            else:
                motion += [self.__try_to_float(v) for v in lines[i].split()]

        n = len(self.channels)
        new_motion = [motion[i:i+n] for i in range(0, len(motion), n)]

        return (frame_time, frames, new_motion)

    def __getDefaultMotionDataframe(self, motion):
        '''
            BVHファイルからモーションデータを取得する

            Returns
            -------
            pandas.DataFrame
                モーションデータ
        '''

        motion_df = pd.DataFrame(motion)
        motion_df.columns = self.channels
        time = np.arange(0, motion_df.shape[0]) * self.frame_time
        motion_df.insert(0, 'time', time)
        for column in motion_df.columns:
            motion_df[column] = pd.to_numeric(
                motion_df[column], errors='coerce')

        return motion_df

    def getInitialPosition(self, channel_names=['Xposition', 'Yposition', 'Zposition']):
        '''
            初期位置を設定する

            Parameters
            ----------
            position : list
                初期位置
        '''

        motion_df = self.default_motion_df.copy()
        return [motion_df[f'{self.root}_{channel_name}'][0] for channel_name in channel_names]

    def setInitialPosition(self, position, channel_names=['Xposition', 'Yposition', 'Zposition']):
        '''
            初期位置を設定する

            Parameters
            ----------
            position : list
                初期位置
        '''

        motion_df = self.default_motion_df.copy()
        for i, channel_name in enumerate(channel_names):
            motion_df[f'{self.root}_{channel_name}'] = position[i]

        self.motion_df = motion_df

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

        return self.motion_df.copy()

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

    def getChannels(self):
        '''
            チャンネル名のリストを取得する

            Returns
            -------
            list
                チャンネル名のリスト
        '''

        return self.channels
