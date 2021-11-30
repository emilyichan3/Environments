from datetime import date
from flaskapp_env import db
from flaskapp_env.modules_TIA import Term


def get_usable_data(term_id):

    Year = date.today().strftime('%Y')
    year = date.today().strftime('%y')
    month = date.today().strftime('%m')
    current_term = Term.query.filter_by(id=term_id).first()
    
    if current_term is None:
        return None

    next_seq = current_term.Member_NextSeq
    member_id = current_term.Member_Pre + year + current_term.Term + '{:03d}'.format(next_seq)
    current_term.Member_NextSeq = next_seq + 1
    db.session.commit()
    period = Year + month

    return member_id, period
