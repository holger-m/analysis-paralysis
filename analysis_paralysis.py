import argparse
import numpy as np
import itertools
from multiprocessing import Pool

def cards_str_to_bin(card_list):
    
    value_str_order = 'AKQJT98765432'
    suit_str_order = 'cshd'
    
    cards_bin = np.zeros((14, 4), dtype=int)
    
    for i in range(len(card_list)):
        value_ind = value_str_order.find(card_list[i][0])
        suit_ind = suit_str_order.find(card_list[i][1])
        cards_bin[value_ind, suit_ind] = 1
        if value_ind == 0:
            cards_bin[13, suit_ind] = 1
    return cards_bin

def cards_bin_to_hand(cards_bin):
    
    value_str_order = 'AKQJT98765432'
    suit_str_order = 'cshd'
    
    royal_flush_flag = False
    for j in range(4):
        if np.sum(cards_bin[0:5, j]) == 5:
            royal_flush_flag = True
            break
    if royal_flush_flag:
        #print('royal flush')
        hand_list = [0, 0, 0, 0, 0, 0]
        return hand_list
    
    straight_flush_flag = False
    for j in range(4):
        for i in range(1, 10):
            if np.sum(cards_bin[i:i+5, j]) == 5:
                straight_flush_flag = True
                break
        if straight_flush_flag:
            break
    if straight_flush_flag:
        #print('straight flush')
        #print('starting with ' + value_str_order[i])
        hand_list = [1, i, 0, 0, 0, 0]
        return hand_list
    
    foak_flag = False
    for i in range(13):
        if np.sum(cards_bin[i]) == 4:
            foak_flag = True
            for j in range(4):
                cards_bin[i,j] = 0
            kicker_flag = False
            for k in range(13):
                for j in range(4):
                    if cards_bin[k,j] == 1:
                        kicker_flag = True
                        break
                if kicker_flag:
                    break
            break
    if foak_flag:
        #print('four of a kind')
        #print('consisting of ' + value_str_order[i])
        #print('kicker is ' + value_str_order[k])
        hand_list = [2, i, k, 0, 0, 0]
        return hand_list
    
    fh_flag = False
    for i in range(13):
        if np.sum(cards_bin[i]) == 3:
            cards_bin_copy = np.copy(cards_bin)
            for j in range(4):
                cards_bin_copy[i,j] = 0
            for k in range(13):
                if np.sum(cards_bin_copy[k]) >= 2:
                    fh_flag = True
                    break                    
            break
    if fh_flag:
        #print('full house')
        #print('with three ' + value_str_order[i])
        #print('and two ' + value_str_order[k])
        hand_list = [3, i, k, 0, 0, 0]
        return hand_list
    
    flush_flag = False
    for j in range(4):
        if np.sum(cards_bin[0:13,j]) >= 5:
            flush_flag = True
            flush_ind_vec = list()
            for i in range(13):
                if cards_bin[i,j] == 1:
                    flush_ind_vec.append(i)
                    if len(flush_ind_vec) == 5:
                        break
            break
    if flush_flag:
        #print('flush')
        #print('with ' + value_str_order[flush_ind_vec[0]]
        #              + value_str_order[flush_ind_vec[1]]
        #              + value_str_order[flush_ind_vec[2]]
        #              + value_str_order[flush_ind_vec[3]]
        #              + value_str_order[flush_ind_vec[4]])
        hand_list = [4, flush_ind_vec[0],
                        flush_ind_vec[1],
                        flush_ind_vec[2],
                        flush_ind_vec[3],
                        flush_ind_vec[4]]
        return hand_list

    straight_flag = False
    cards_bin_sum_suits = np.zeros((14,), dtype=int)
    for i in range(14):
        if np.sum(cards_bin[i, :]) >= 1:
            cards_bin_sum_suits[i] = 1
    for i in range(10):
        if np.sum(cards_bin_sum_suits[i:i+5]) == 5:
            straight_flag = True
            break
    if straight_flag:
        #print('straight')
        #print('starting with ' + value_str_order[i])
        hand_list = [5, i, 0, 0, 0, 0]
        return hand_list

    toak_flag = False
    for i in range(13):
        if np.sum(cards_bin[i]) == 3:
            toak_flag = True
            for j in range(4):
                cards_bin[i,j] = 0
            kicker_inds = list()
            kicker_flag = False
            for k in range(13):
                for j in range(4):
                    if cards_bin[k,j] == 1:
                        kicker_inds.append(k)
                        if len(kicker_inds) == 2:
                            kicker_flag = True
                            break
                if kicker_flag:
                    break
            break
    if toak_flag:
        #print('three of a kind')
        #print('with three ' + value_str_order[i])
        #print('and kicker ' + value_str_order[kicker_inds[0]] + ' and '
        #                    + value_str_order[kicker_inds[1]])
        hand_list = [6, i, kicker_inds[0], kicker_inds[1], 0, 0]
        return hand_list

    two_pair_flag = False
    one_pair_flag = False
    for i in range(13):
        if np.sum(cards_bin[i]) == 2:
            one_pair_flag = True
            for j in range(4):
                cards_bin[i,j] = 0
            for k in range(i+1, 13):
                if np.sum(cards_bin[k]) == 2:
                    two_pair_flag = True
                    one_pair_flag = False
                    for j in range(4):
                        cards_bin[k,j] = 0
                    break
            break
    if one_pair_flag:
        kicker_inds = list()
        kicker_flag = False
        for m in range(13):
            for j in range(4):
                if cards_bin[m,j] == 1:
                    kicker_inds.append(m)
                    if len(kicker_inds) == 3:
                        kicker_flag = True
                        break
            if kicker_flag:
                break
    if two_pair_flag:
        kicker_inds = list()
        kicker_flag = False
        for m in range(13):
            for j in range(4):
                if cards_bin[m,j] == 1:
                    kicker_inds.append(m)
                    if len(kicker_inds) == 1:
                        kicker_flag = True
                        break
            if kicker_flag:
                break
    if two_pair_flag:
        #print('two pair')
        #print('with pairs ' + value_str_order[i] + ' and ' + value_str_order[k])
        #print('and kicker ' + value_str_order[kicker_inds[0]])
        hand_list = [7, i, k, kicker_inds[0], 0, 0]
        return hand_list
    if one_pair_flag:
        #print('one pair')
        #print('with pair ' + value_str_order[i] )
        #print('and kicker ' + value_str_order[kicker_inds[0]] + ' and '
        #                    + value_str_order[kicker_inds[1]] + ' and '
        #                    + value_str_order[kicker_inds[2]])
        hand_list = [8, i, kicker_inds[0], kicker_inds[1], kicker_inds[2], 0]
        return hand_list

    no_hand_flag = False
    no_hand_ind_vec = list()
    for i in range(13):
        for j in range(4):
            if cards_bin[i,j] == 1:
                no_hand_ind_vec.append(i)
                if len(no_hand_ind_vec) == 5:
                    no_hand_flag = True
                    break
        if no_hand_flag:
            break
    if no_hand_flag:
        #print('no hand')
        #print('with values ' + value_str_order[no_hand_ind_vec[0]] + ' and '
        #                     + value_str_order[no_hand_ind_vec[1]] + ' and '
        #                     + value_str_order[no_hand_ind_vec[2]] + ' and '
        #                     + value_str_order[no_hand_ind_vec[3]] + ' and '
        #                     + value_str_order[no_hand_ind_vec[4]])
        hand_list = [9, no_hand_ind_vec[0],
                        no_hand_ind_vec[1],
                        no_hand_ind_vec[2],
                        no_hand_ind_vec[3],
                        no_hand_ind_vec[4]]
        return hand_list

def compare_hands(hand_1, hand_2):
    for i in range(6):
        if hand_1[i] < hand_2[i]:
            result_ind = 0 # hand 1 wins
            return result_ind
        if hand_1[i] > hand_2[i]:
            result_ind = 1 # hand 2 wins
            return result_ind
    result_ind = 2 # equal hands
    return result_ind
    
def play_out_hand(subset_tuple, cards_in_stack_3D_bin, p1_bin, p2_bin, board_cards_bin):
    
    subset_cards_bin = np.sum(cards_in_stack_3D_bin[:,:,subset_tuple], axis=2)
    #print(subset_cards_bin.shape)
    
    p1_7_cards_bin = p1_bin + board_cards_bin + subset_cards_bin
    #print(p1_7_cards_bin)
    p2_7_cards_bin = p2_bin + board_cards_bin + subset_cards_bin
    #print(p2_7_cards_bin)
    
    p1_hand = cards_bin_to_hand(p1_7_cards_bin)
    #print(p1_hand)
    p2_hand = cards_bin_to_hand(p2_7_cards_bin)
    #print(p2_hand)
    
    result_ind = compare_hands(p1_hand, p2_hand)
    #print(result_ind)
    return result_ind

def go_through_list_of_subsets(list_of_card_subsets, 
                               cards_in_stack_3D_bin, 
                               p1_bin, 
                               p2_bin, 
                               board_cards_bin):
    
    player_1_win_count = 0
    player_2_win_count = 0
    split_pot_count = 0
    
    for subset_ind in range(len(list_of_card_subsets)):
        
        if (subset_ind + 1) % 10000 == 0 or (subset_ind + 1) == len(list_of_card_subsets):
            print(' ')
            print(str(subset_ind + 1) + ' of ' + str(len(list_of_card_subsets)))
            print(str(100*(subset_ind + 1)/len(list_of_card_subsets)) + ' percent')
        
        subset_tuple = list_of_card_subsets[subset_ind]
        
        result_ind = play_out_hand(subset_tuple, 
                                   cards_in_stack_3D_bin, 
                                   p1_bin, 
                                   p2_bin, 
                                   board_cards_bin)
        
        if result_ind == 0:
            player_1_win_count += 1
            #print('player 1 wins')
        elif result_ind == 1:
            player_2_win_count += 1
            #print('player 2 wins')
        elif result_ind == 2:
            split_pot_count += 1
            #print('split pot')
            
    return player_1_win_count, player_2_win_count, split_pot_count

def go_through_list_of_subsets_global(list_of_card_subsets):
    
    player_1_win_count = 0
    player_2_win_count = 0
    player_3_win_count = 0
    player_1_split_pot_count = 0
    player_2_split_pot_count = 0
    player_3_split_pot_count = 0
    
    for subset_ind in range(len(list_of_card_subsets)):
        
        if (subset_ind + 1) % 10000 == 0 or (subset_ind + 1) == len(list_of_card_subsets):
            print(' ')
            print(str(subset_ind + 1) + ' of ' + str(len(list_of_card_subsets)))
            print(str(100*(subset_ind + 1)/len(list_of_card_subsets)) + ' percent')
        
        subset_tuple = list_of_card_subsets[subset_ind]
        
        result_ind_1_2 = play_out_hand(subset_tuple, 
                                   cards_in_stack_3D_bin_global, 
                                   p1_bin_global, 
                                   p2_bin_global, 
                                   board_cards_bin_global)
        
        result_ind_1_3 = play_out_hand(subset_tuple, 
                                   cards_in_stack_3D_bin_global, 
                                   p1_bin_global, 
                                   p3_bin_global, 
                                   board_cards_bin_global)
        
        result_ind_2_3 = play_out_hand(subset_tuple, 
                                   cards_in_stack_3D_bin_global, 
                                   p2_bin_global, 
                                   p3_bin_global, 
                                   board_cards_bin_global)
        
        if result_ind_1_2 == 0 and result_ind_1_3 == 0:
            player_1_win_count += 1
            #print('player 1 wins')
        elif result_ind_1_2 == 1 and result_ind_2_3 == 0:
            player_2_win_count += 1
            #print('player 2 wins')
        elif result_ind_1_3 == 1 and result_ind_2_3 == 1:
            player_3_win_count += 1
            #print('player 3 wins')
        elif result_ind_1_2 == 0 and result_ind_1_3 == 2 and result_ind_2_3 == 1:
            player_1_split_pot_count += 1
            player_3_split_pot_count += 1
            #print('split pot P1 P3')
        elif result_ind_1_2 == 1 and result_ind_1_3 == 1 and result_ind_2_3 == 2:
            player_2_split_pot_count += 1
            player_3_split_pot_count += 1
            #print('split pot P2 P3')
        elif result_ind_1_2 == 2 and result_ind_1_3 == 0 and result_ind_2_3 == 0:
            player_1_split_pot_count += 1
            player_2_split_pot_count += 1
            #print('split pot P1 P2')
        elif result_ind_1_2 == 2 and result_ind_1_3 == 2 and result_ind_2_3 == 2:
            player_1_split_pot_count += 1
            player_2_split_pot_count += 1
            player_3_split_pot_count += 1
            #print('split pot P1 P2 P3')
        else:
            raise Exception('Invalid hand comparison!')
    
    return_list = list()
    return_list.append(player_1_win_count)
    return_list.append(player_2_win_count)
    return_list.append(player_3_win_count)
    return_list.append(player_1_split_pot_count)
    return_list.append(player_2_split_pot_count)
    return_list.append(player_3_split_pot_count)
            
    return return_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p1', '--player_1', help='XNAT URL', type=str, required=True)
    parser.add_argument('-p2', '--player_2', help='XNAT URL', type=str, required=True)
    parser.add_argument('-p3', '--player_3', help='XNAT URL', type=str)
    parser.add_argument('-f', '--flop', help='XNAT URL', type=str)
    parser.add_argument('-t', '--turn', help='XNAT URL', type=str)
    parser.add_argument('-r', '--river', help='XNAT URL', type=str)
    parser.add_argument('-c', '--cpu', help='XNAT URL', type=int, required=True)
    args = parser.parse_args()
    
    p1_list = [args.player_1[0:2], args.player_1[2:4]]
    p1_bin = cards_str_to_bin(p1_list)
    
    p2_list = [args.player_2[0:2], args.player_2[2:4]]
    p2_bin = cards_str_to_bin(p2_list)
    
    
    if args.player_3:
        p3_list = [args.player_3[0:2], args.player_3[2:4]]
        p3_bin = cards_str_to_bin(p3_list)
    else:
        p3_bin = np.zeros((14, 4), dtype=int)
    
    if args.flop:
        flop_list = [args.flop[0:2], args.flop[2:4], args.flop[4:6]]
        flop_bin = cards_str_to_bin(flop_list)
    else:
        flop_bin = np.zeros((14, 4), dtype=int)
    
    if args.turn:
        turn_list = [args.turn[0:2]]
        turn_bin = cards_str_to_bin(turn_list)
    else:
        turn_bin = np.zeros((14, 4), dtype=int)
    
    if args.river:
        river_list = [args.river[0:2]]
        river_bin = cards_str_to_bin(river_list)
    else:
        river_bin = np.zeros((14, 4), dtype=int)

    cards_in_stack_bin = np.ones((14, 4), dtype=int) - p1_bin - p2_bin - p3_bin \
                         - flop_bin - turn_bin - river_bin
    #print(cards_in_stack_bin)
    no_of_cards_in_stack = np.sum(np.sum(cards_in_stack_bin[0:13,:]))
    #print(no_of_cards_in_stack)

    cards_in_stack_3D_bin = np.zeros((14, 4, no_of_cards_in_stack), dtype=int)
    card_count = 0
    for i in range(13):
        for j in range(4):
            if cards_in_stack_bin[i,j] == 1:
                cards_in_stack_3D_bin[i,j,card_count] = 1
                if i == 0:
                    cards_in_stack_3D_bin[13,j,card_count] = 1
                card_count += 1

    board_cards_bin = flop_bin + turn_bin + river_bin
    
    no_of_cards_unknown = 5 - np.sum(np.sum(board_cards_bin[0:13,:]))
    #print(no_of_cards_unknown)

    list_of_card_subsets = list(itertools.combinations(range(no_of_cards_in_stack), 
                                                       no_of_cards_unknown))
    #print(list_of_card_subsets)
    
    length_per_process = len(list_of_card_subsets)//args.cpu
    print(length_per_process)
    process_lists_list = list()
    for proc_int in range(args.cpu):
        start_ind = proc_int*length_per_process
        end_ind = (proc_int + 1)*length_per_process
        if proc_int + 1 == args.cpu:
            end_ind = len(list_of_card_subsets)
        #print(' ')
        #print(start_ind)
        #print(end_ind)
        process_lists_list.append(list_of_card_subsets[start_ind:end_ind])
    #for proc_int in range(args.cpu):
    #    print(' ')
    #    print(process_lists_list[proc_int])
    
    global cards_in_stack_3D_bin_global
    cards_in_stack_3D_bin_global = np.copy(cards_in_stack_3D_bin)
    global p1_bin_global
    p1_bin_global = np.copy(p1_bin)
    global p2_bin_global
    p2_bin_global = np.copy(p2_bin)
    global p3_bin_global
    p3_bin_global = np.copy(p3_bin)
    global board_cards_bin_global
    board_cards_bin_global = np.copy(board_cards_bin)
    
    return_lists_list = list()
    
    pool = Pool(processes=args.cpu)
    for proc_int in range(args.cpu):
        return_lists_list.append(pool.apply_async(go_through_list_of_subsets_global, 
                                   [process_lists_list[proc_int]]))
    #return_list0 = pool.apply_async(go_through_list_of_subsets_global, 
    #                               [process_lists_list[0]])
    #return_list1 = pool.apply_async(go_through_list_of_subsets_global, 
    #                               [process_lists_list[1]])
    #return_list2 = pool.apply_async(go_through_list_of_subsets_global, 
    #                               [process_lists_list[2]])
    #return_list3 = pool.apply_async(go_through_list_of_subsets_global, 
    #                               [process_lists_list[3]])
    
    pool.close()
    pool.join()
    
    player_1_win_count = 0
    player_2_win_count = 0
    player_3_win_count = 0
    player_1_split_pot_count = 0
    player_2_split_pot_count = 0
    player_3_split_pot_count = 0
    
    for proc_int in range(args.cpu):
        player_1_win_count += return_lists_list[proc_int].get()[0]
        player_2_win_count += return_lists_list[proc_int].get()[1]
        player_3_win_count += return_lists_list[proc_int].get()[2]
        player_1_split_pot_count += return_lists_list[proc_int].get()[3]
        player_2_split_pot_count += return_lists_list[proc_int].get()[4]
        player_3_split_pot_count += return_lists_list[proc_int].get()[5]
    #print(return_list0.get())
    #print(return_list1.get())
    #print(return_list2.get())
    #print(return_list3.get())

    #player_1_win_count, player_2_win_count, split_pot_count = go_through_list_of_subsets(
    #                                                             process_lists_list[0], 
    #                                                             cards_in_stack_3D_bin, 
    #                                                             p1_bin, 
    #                                                             p2_bin, 
    #                                                             board_cards_bin)
    
    player_1_loss_count = len(list_of_card_subsets) - player_1_win_count - player_1_split_pot_count
    player_2_loss_count = len(list_of_card_subsets) - player_2_win_count - player_2_split_pot_count
    player_3_loss_count = len(list_of_card_subsets) - player_3_win_count - player_3_split_pot_count
    
    print(' ')
    print('player 1 percent win/lose/split:')
    print(player_1_win_count/len(list_of_card_subsets))
    print(player_1_loss_count/len(list_of_card_subsets))
    print(player_1_split_pot_count/len(list_of_card_subsets))
    print(' ')
    print('player 2 percent win/lose/split:')
    print(player_2_win_count/len(list_of_card_subsets))
    print(player_2_loss_count/len(list_of_card_subsets))
    print(player_2_split_pot_count/len(list_of_card_subsets))
    print(' ')
    print('player 3 percent win/lose/split:')
    print(player_3_win_count/len(list_of_card_subsets))
    print(player_3_loss_count/len(list_of_card_subsets))
    print(player_3_split_pot_count/len(list_of_card_subsets))
    print(' ')

if __name__ == '__main__':
    main()
