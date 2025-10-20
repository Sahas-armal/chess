from flask import Blueprint, render_template, request
import os
import chess_review  

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template('index.html')  

@views.route('/analysis', methods=['POST'])
def analyse():
    roast = False
    if request.method == 'POST':
        pgn_data = request.form.get('pgn', '')  
        roast = 'roastmode' in request.form  

    # the previous problem solved this is to Ensure `chess_review` functions exist and are working
    try:
        uci_moves, san_moves, fens = chess_review.parse_pgn(pgn_data)
        scores, cpls_white, cpls_black, avg_cpl_white, avg_cpl_black = chess_review.compute_cpl(uci_moves, time_limit=0.05)
        n_moves = len(scores) // 2
        white_elo, black_elo = chess_review.estimate_elo(avg_cpl_white, n_moves), chess_review.estimate_elo(avg_cpl_black, n_moves)
        white_acc, black_acc = chess_review.calculate_accuracy(scores)
        devs, mobs, tens, conts = chess_review.calculate_metrics(fens)
        review_list, best_review_list, classification_list, uci_best_moves, san_best_moves = chess_review.review_game(uci_moves, roast)
        uci_best_moves = chess_review.seperate_squares_in_move_list(uci_best_moves)

        return render_template(
            'analysis.html',
            move_list=san_moves,
            fen_list=fens,
            score_list=scores,
            cls_list=classification_list,
            review_list=review_list,
            best_review_list=best_review_list,
            best_move_list=san_best_moves,
            best_move_uci_list=uci_best_moves,
            dev_list=devs,
            ten_list=tens,
            mob_list=mobs,
            cont_list=conts,
            acc_pair=[round(white_acc), round(black_acc)],
            elo_pair=[round(white_elo), round(black_elo)],
            acpl_pair=[round(avg_cpl_white), round(avg_cpl_black)]
        )

    except Exception as e:
        return f"Error processing analysis: {e}", 500  #  Handle errors properly
