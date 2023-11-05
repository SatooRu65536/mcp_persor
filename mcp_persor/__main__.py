from .persor import BVHparser
from .plot import plot

bvhp = BVHparser('sample/jump.bvh')
motion_df = bvhp.getMotionDataframe()

joint_name = 'r_toes'

relative_motion_df = bvhp.getRelativeMotionDataframe(joint_name)
absolute_motion_df = bvhp.getAbsoluteMotionDataframe(joint_name)

plot(
    df=relative_motion_df,
    heads=[
        ['time', 'Xposition'],
        ['time', 'Yposition'],
        ['time', 'Zposition']
    ],
    title=f'相対的な {joint_name} の位置',
    xlabel='time [s]',
    ylabel='position [m]',
    xlim=[0, 0],
    ylim=[0, 0],
    grid=True,
)

plot(
    df=absolute_motion_df,
    heads=[
        ['time', 'Xposition'],
        ['time', 'Yposition'],
        ['time', 'Zposition']
    ],
    title=f'絶対的な {joint_name} の位置',
    xlabel='time [s]',
    ylabel='position [m]',
    xlim=[0, 0],
    ylim=[0, 0],
    grid=True,
)
