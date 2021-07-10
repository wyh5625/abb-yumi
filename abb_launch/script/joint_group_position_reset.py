#! /usr/bin/env python

"""
rosservice call /controller_manager/switch_controller "start_controllers: ['joint_group_pos_controller']
stop_controllers: ['joint_group_vel_controller']
strictness: 1
start_asap: false
timeout: 0.0"
"""

import rospy
from std_msgs.msg import Float64MultiArray


if __name__ == '__main__':
    rospy.init_node('joint_group_position_reset')

    js_pub = rospy.Publisher('/yumi/joint_group_position_controller/command', Float64MultiArray, queue_size=1)
    joint_group_position = Float64MultiArray()
    #     - yumi_joint_1_l
    #     - yumi_joint_2_l
    #     - yumi_joint_7_l
    #     - yumi_joint_3_l
    #     - yumi_joint_4_l
    #     - yumi_joint_5_l
    #     - yumi_joint_6_l
    #     - yumi_joint_1_r
    #     - yumi_joint_2_r
    #     - yumi_joint_7_r
    #     - yumi_joint_3_r
    #     - yumi_joint_4_r
    #     - yumi_joint_5_r
    #     - yumi_joint_6_r
    # TODO: change the data!!!!
    joint_group_position.data = [0,0,0,0,0,0,0,
                                 0,0,0,0,0,0,0]
    js_pub.publish()

    rospy.sleep(1)
