from mcp_persor.persor import BVHparser
from mcp_persor.plot import plot

bvhp = BVHparser('bvh/jump.bvh')
motion_df = bvhp.getMotionDataframe()

joint_name = 'head'

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
    df=relative_motion_df,
    heads=[
        ['time', 'Xrotation'],
        ['time', 'Yrotation'],
        ['time', 'Zrotation']
    ],
    title=f'相対的な {joint_name} の回転',
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

plot(
    df=absolute_motion_df,
    heads=[
        ['time', 'Xrotation'],
        ['time', 'Yrotation'],
        ['time', 'Zrotation']
    ],
    title=f'絶対的な {joint_name} の回転',
    xlabel='time [s]',
    ylabel='position [m]',
    xlim=[0, 0],
    ylim=[0, 0],
    grid=True,
)
