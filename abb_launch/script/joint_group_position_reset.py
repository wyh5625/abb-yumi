#! /usr/bin/env python3

"""
rosservice call /controller_manager/switch_controller "start_controllers: ['joint_group_pos_controller']
stop_controllers: ['joint_group_vel_controller']
strictness: 1
start_asap: false
timeout: 0.0"
"""

import rospy
from std_msgs.msg import Float64MultiArray
from controller_manager_msgs.srv import SwitchController


def switch(start_controllers, stop_controllers):
    service_name = '/yumi/controller_manager/switch_controller'
    rospy.wait_for_service(service_name)
    BEST_EFFORT = 1
    STRICT = 2
    try:
        switch_controller = rospy.ServiceProxy(service_name, SwitchController)
        # start_controllers= ['joint_group_pos_controller']
        # stop_controllers=['joint_group_vel_controller']
        strictness=BEST_EFFORT
        start_asap=False
        timeout=0.0
        resp = switch_controller(start_controllers, stop_controllers, strictness, start_asap, timeout)
        rospy.loginfo(f'switch -- start: {start_controllers}, stop:{stop_controllers}, resp.ok: {resp.ok}')
        return resp.ok
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def re_order(data_in):
    data_out = [0]*14
    data_out[0] = data_in[0]
    data_out[1] = data_in[2]
    data_out[2] = data_in[-2]
    data_out[3] = data_in[4]
    data_out[4] = data_in[6]
    data_out[5] = data_in[8]
    data_out[6] = data_in[10]

    data_out[7] = data_in[1]
    data_out[8] = data_in[3]
    data_out[9] = data_in[-1]
    data_out[10] = data_in[5]
    data_out[11] = data_in[7]
    data_out[12] = data_in[9]
    data_out[13] = data_in[11]

    return data_out

if __name__ == '__main__':
    rospy.init_node('joint_group_position_reset')

    switch(['joint_group_pos_controller'], ['joint_group_vel_controller'])

    js_pub = rospy.Publisher('/yumi/joint_group_pos_controller/command', Float64MultiArray, queue_size=1,latch=True)
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
    #joint_group_position.data = [-0.81, -0.75,  1.69,  0.34, -0.36, 0.92, -0.43,  1.08, -1.74, -1.06, 0.50, -1.22,  1.34,  1.58]


    #joint_group_position.data = re_order([-0.7459468245506287, 0.9288483262062073, -0.7346209287643433, -1.7862653732299805, 0.46832385659217834, 0.6180986166000366, -0.4357328712940216, -1.2335011959075928, 0.9003364443778992, 1.2640312910079956, -0.2185577154159546, 1.5123498439788818, 1.798527479171753, -1.1854052543640137])

    # overhead position
    joint_group_position.data = re_order([-1.0230605602264404, 1.0736857652664185, -0.8376967310905457, -1.7577592134475708, 0.20048120617866516, 0.4010566174983978, -0.2610374093055725, -1.2049086093902588, 0.9034560918807983, 1.405629277229309, -0.47287923097610474, 1.475947380065918, 1.8396306037902832, -1.0484275817871094])
    js_pub.publish(joint_group_position)

    rospy.sleep(2)

    # upper right
    #joint_group_position.data = re_order([-1.1096142530441284, 1.3619880676269531, -0.7512943744659424, -1.5642908811569214, 0.1181102842092514, -0.01239237654954195, -0.15036740899085999, -1.1789796352386475, 0.866365373134613, 1.6377902030944824, -0.8806593418121338, 1.4989044666290283, 1.5641430616378784, -0.791698694229126])
    
    # lower center
    #joint_group_position.data = re_order([-0.7459468245506287, 0.9288483262062073, -0.7346209287643433, -1.7862653732299805, 0.46832385659217834, 0.6180986166000366, -0.4357328712940216, -1.2335011959075928, 0.9003364443778992, 1.2640312910079956, -0.2185577154159546, 1.5123498439788818, 1.798527479171753, -1.1854052543640137])
    
    # upper left 
    #joint_group_position.data = re_order([-1.2117047309875488, 1.6358189582824707, -0.8566433191299438, -1.5167449712753296, -0.6169570088386536, 0.13077692687511444, -0.052748728543519974, -1.350795030593872, 1.5248706340789795, 1.3757778406143188, -0.8875612020492554, 1.8182926177978516, 1.6703616380691528, -0.9605697393417358])
    
    # lower left
    joint_group_position.data = re_order([-0.6704050302505493, 1.1032830476760864, -0.8577622175216675, -1.8114362955093384, 0.17825478315353394, 0.8806893229484558, -0.19923526048660278, -1.5176565647125244, 1.202042579650879, 1.16306471824646, -0.38206374645233154, 1.9358222484588623, 1.768209457397461, -1.2573240995407104])


    # lower right
    #joint_group_position.data = re_order([-0.9556007385253906, 0.7370144128799438, -0.7808167338371277, -1.7906967401504517, 0.7637262940406799, 0.4180224537849426, -0.6161741018295288, -1.0667353868484497, 0.4623887240886688, 1.4415569305419922, -0.05812250077724457, 1.1671340465545654, 1.8294209241867065, -1.169150948524475])

    # right
    #joint_group_position.data = re_order([-1.0409072637557983, 1.0751211643218994, -0.7609612941741943, -1.7107101678848267, 0.5152636766433716, 0.18548442423343658, -0.32017719745635986, -1.1102017164230347, 0.5475361943244934, 1.6092324256896973, -0.6015754342079163, 1.3619227409362793, 1.6255568265914917, -0.8875283002853394])

    js_pub.publish(joint_group_position)

    rospy.loginfo("reset position")
    rospy.sleep(3)

    switch(['joint_group_vel_controller'], ['joint_group_pos_controller'])
    rospy.sleep(1)


