import pandas as pd


class BVHparser:
    def __init__(self, filename):
        self.bvh = self.__readFile(filename)
        self.frame_time = self.__getFrameTime()
        self.skeleton = self.__getSkeleton()

    def __readFile(self, filename):
        with open(filename, 'r') as f:
            return f.read()

    def __getFrameTime(self):
        for token in self.bvh.split('Frame Time:')[1].split():
            if token != '':
                return float(token)

    def __getMotion(self):
        motion = self.bvh.split('Frame Time:')[1]
        motion = motion.split("\n")
        return motion[1:]

    def __getSkeleton(self):
        return {
            'root': {'id': 0, 'joint': None},
            'torso_1': {'id': 1, 'joint': 'root'},
            'torso_2': {'id': 2, 'joint': 'torso_1'},
            'torso_3': {'id': 3, 'joint': 'torso_2'},
            'torso_4': {'id': 4, 'joint': 'torso_3'},
            'torso_5': {'id': 5, 'joint': 'torso_4'},
            'torso_6': {'id': 6, 'joint': 'torso_5'},
            'torso_7': {'id': 7, 'joint': 'torso_6'},
            'neck_1': {'id': 8, 'joint': 'torso_7'},
            'neck_2': {'id': 9, 'joint': 'neck_1'},
            'head': {'id': 10, 'joint': 'neck_2'},
            'l_shoulder': {'id': 11, 'joint': 'torso_7'},
            'l_up_arm': {'id': 12, 'joint': 'l_shoulder'},
            'l_low_arm': {'id': 13, 'joint': 'l_up_arm'},
            'l_hand': {'id': 14, 'joint': 'l_low_arm'},
            'r_shoulder': {'id': 15, 'joint': 'torso_7'},
            'r_up_arm': {'id': 16, 'joint': 'r_shoulder'},
            'r_low_arm': {'id': 17, 'joint': 'r_up_arm'},
            'r_hand': {'id': 18, 'joint': 'r_low_arm'},
            'l_up_leg': {'id': 19, 'joint': 'root'},
            'l_low_leg': {'id': 20, 'joint': 'l_up_leg'},
            'l_foot': {'id': 21, 'joint': 'l_low_leg'},
            'l_toes': {'id': 22, 'joint': 'l_foot'},
            'r_up_leg': {'id': 23, 'joint': 'root'},
            'r_low_leg': {'id': 24, 'joint': 'r_up_leg'},
            'r_foot': {'id': 25, 'joint': 'r_low_leg'},
            'r_toes': {'id': 26, 'joint': 'r_foot'},
        }

    def getSkeletonPathToRoot(self, joint):
        path = []
        while joint != None:
            path.append(joint)
            joint = self.skeleton[joint]['joint']
        return path

    def getMotionDataframe(self):
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
        motion_df = self.getMotionDataframe()
        path = self.getSkeletonPathToRoot(joint)
        print(path)

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
