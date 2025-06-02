from PythonExpenseApp.db_connection import DbConnection
import re

class Statistics:
    def __init__(self, activities=None, feedbacks=None):
        self.activities = activities or {}
        self.feedbacks = feedbacks or {}

    def get_total_participants(self):
        return sum(len(students) for students in self.activities.values())

    def get_most_popular_activity(self):
        if not self.activities:
            return None
        return max(self.activities, key=lambda act: len(self.activities[act]))

    def highlight_sentimental_words(self, activity, sentimental_words):
        feedback_list = self.feedbacks.get(activity, [])
        highlighted = []
        for feedback in feedback_list:
            highlighted_feedback = feedback
            for word in sentimental_words:
                # Add asterisks around matching words
                pattern = r"\b" + re.escape(word) + r"\b"
                highlighted_feedback = re.sub(pattern, f"*{word}*", highlighted_feedback)
            highlighted.append(highlighted_feedback)
        return highlighted

    def get_average_participants(self):
        if not self.activities:
            return 0.0
        return float(self.get_total_participants()) / len(self.activities)

    def fetch_statistics_from_database(self):
        """Fetch comprehensive statistics from database"""
        stats = {}
        
        # Total participants across all activities
        query = "SELECT COUNT(*) AS total_participants FROM student_activities"
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['total_participants'] = result[0]
        
        # Most popular activity
        query = """SELECT a.name, COUNT(sa.student_id) as participant_count
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name
                   ORDER BY participant_count DESC
                   LIMIT 1"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['most_popular_activity'] = {'name': result[0], 'participants': result[1]}
        
        # Activity participation statistics
        query = """SELECT a.name, COUNT(sa.student_id) as participants, a.max_participants
                   FROM activities a
                   LEFT JOIN student_activities sa ON a.id = sa.activity_id
                   GROUP BY a.id, a.name, a.max_participants
                   ORDER BY participants DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_participation'] = result
        
        # Average rating per activity
        query = """SELECT a.name, AVG(f.rating) as avg_rating, COUNT(f.id) as feedback_count
                   FROM activities a
                   LEFT JOIN feedback f ON a.id = f.activity_id
                   GROUP BY a.id, a.name
                   HAVING feedback_count > 0
                   ORDER BY avg_rating DESC"""
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            stats['activity_ratings'] = result
        
        # Total expenses and debt statistics
        query = """SELECT 
                       SUM(amount) as total_expenses,
                       COUNT(*) as expense_count,
                       AVG(amount) as avg_expense
                   FROM expenses"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['expense_summary'] = {
                'total': result[0] if result[0] else 0,
                'count': result[1],
                'average': result[2] if result[2] else 0
            }
        
        # Outstanding debts summary
        query = """SELECT 
                       SUM(amount) as total_outstanding,
                       COUNT(*) as debt_count
                   FROM debts WHERE paid = FALSE"""
        success, result = DbConnection.execute_query(query, fetch_one=True)
        if success and result:
            stats['debt_summary'] = {
                'total_outstanding': result[0] if result[0] else 0,
                'count': result[1]
            }
        
        return stats

    def get_student_statistics(self, student_id):
        """Get statistics for a specific student"""
        stats = {}
        
        # Student's activities
        query = """SELECT COUNT(*) FROM student_activities WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['activities_count'] = result[0]
        
        # Student's expenses (as payer)
        query = """SELECT COUNT(*), SUM(amount) FROM expenses WHERE id_giver = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['expenses_paid'] = {
                'count': result[0],
                'total': result[1] if result[1] else 0
            }
        
        # Money owed to student
        query = """SELECT SUM(amount) FROM debts WHERE payer_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_owed_to_student'] = result[0] if result[0] else 0
        
        # Money student owes
        query = """SELECT SUM(amount) FROM debts WHERE debtor_id = %s AND paid = FALSE"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['money_student_owes'] = result[0] if result[0] else 0
        
        # Student's feedback count
        query = """SELECT COUNT(*) FROM feedback WHERE student_id = %s"""
        success, result = DbConnection.execute_query(query, (student_id,), fetch_one=True)
        if success and result:
            stats['feedback_given'] = result[0]
        
        return stats

    def get_sentiment_words_for_activity(self, activity_id, limit=20):
        """Get most common sentiment words from feedback for a specific activity"""
        query = """SELECT word, frequency, sentiment_type
                   FROM sentiment_words 
                   WHERE activity_id = %s
                   ORDER BY frequency DESC, word
                   LIMIT %s"""
        
        success, result = DbConnection.execute_query(query, (activity_id, limit), fetch_all=True)
        if success:
            return [{'word': row[0], 'frequency': row[1], 'sentiment': row[2]} for row in result]
        return []

    def extract_and_analyze_sentiment_words(self, activity_id):
        """Extract and analyze sentiment words from all feedback for an activity"""
        # Get all feedback comments for the activity
        query = """SELECT comment FROM feedback 
                   WHERE activity_id = %s AND comment IS NOT NULL AND comment != ''"""
        
        success, comments = DbConnection.execute_query(query, (activity_id,), fetch_all=True)
        if not success or not comments:
            return []
        
        word_frequency = {}
        sentiment_dict = self._get_sentiment_dictionary()
        
        # Process each comment
        for (comment,) in comments:
            words = self._extract_words_from_text(comment)
            for word in words:
                if len(word) > 2:  # Filter out very short words
                    word_frequency[word] = word_frequency.get(word, 0) + 1
        
        # Convert to list with sentiment analysis
        sentiment_words = []
        for word, frequency in word_frequency.items():
            sentiment = self._determine_word_sentiment(word, sentiment_dict)
            sentiment_words.append({
                'word': word,
                'frequency': frequency,
                'sentiment': sentiment
            })
        
        # Sort by frequency (most common first)
        sentiment_words.sort(key=lambda x: x['frequency'], reverse=True)
        
        # Update database
        self._update_sentiment_words_in_database(activity_id, sentiment_words)
        
        return sentiment_words

    def _extract_words_from_text(self, text):
        """Extract meaningful words from text"""
        if not text:
            return []
        
        # Convert to lowercase and remove punctuation
        import string
        text = text.lower()
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        
        # Split into words
        words = text.split()
        
        # Filter out common stop words
        stop_words = {
            'the', 'and', 'but', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had',
            'this', 'that', 'with', 'from', 'they', 'them', 'their', 'there', 'where',
            'when', 'what', 'who', 'how', 'why', 'which', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'did', 'does', 'don', 'not',
            'isn', 'wasn', 'weren', 'haven', 'hasn', 'hadn', 'won', 'wouldn',
            'couldn', 'shouldn', 'mustn', 'needn', 'daren', 'mightn', 'shan',
            'very', 'too', 'also', 'just', 'only', 'even', 'much', 'more', 'most',
            'than', 'then', 'now', 'here', 'there', 'into', 'onto', 'upon',
            'about', 'above', 'below', 'under', 'over', 'through', 'during',
            'before', 'after', 'while', 'since', 'until', 'although', 'though',
            'because', 'if', 'unless', 'whether', 'or', 'nor', 'so', 'yet',
            'however', 'therefore', 'thus', 'hence', 'moreover', 'furthermore',
            'nevertheless', 'nonetheless', 'otherwise', 'meanwhile', 'indeed',
            'certainly', 'surely', 'perhaps', 'maybe', 'probably', 'possibly',
            'actually', 'really', 'truly', 'definitely', 'absolutely', 'quite',
            'rather', 'fairly', 'pretty', 'somewhat', 'slightly', 'extremely'
        }
        
        # Filter out stop words and very short words
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        return meaningful_words

    def _get_sentiment_dictionary(self):
        """Get dictionary of words categorized by sentiment"""
        return {
            'positive': {
                'excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'awesome', 
                'perfect', 'beautiful', 'loved', 'enjoyable', 'fun', 'interesting', 
                'good', 'nice', 'pleasant', 'exciting', 'brilliant', 'outstanding',
                'superb', 'magnificent', 'marvelous', 'incredible', 'spectacular',
                'delightful', 'charming', 'lovely', 'attractive', 'impressive',
                'remarkable', 'exceptional', 'extraordinary', 'fabulous', 'gorgeous',
                'splendid', 'terrific', 'thrilling', 'stunning', 'breathtaking',
                'captivating', 'enchanting', 'fascinating', 'engaging', 'absorbing',
                'entertaining', 'amusing', 'hilarious', 'joyful', 'cheerful',
                'happy', 'glad', 'pleased', 'satisfied', 'content', 'comfortable',
                'relaxed', 'peaceful', 'calm', 'serene', 'tranquil', 'refreshing',
                'energizing', 'invigorating', 'inspiring', 'motivating', 'uplifting',
                'encouraging', 'supportive', 'helpful', 'useful', 'valuable',
                'worthwhile', 'beneficial', 'rewarding', 'fulfilling', 'satisfying',
                'successful', 'productive', 'effective', 'efficient', 'smooth',
                'easy', 'simple', 'clear', 'organized', 'well-planned', 'creative',
                'innovative', 'unique', 'special', 'memorable', 'unforgettable'
            },
            'negative': {
                'terrible', 'awful', 'horrible', 'bad', 'worst', 'disappointing',
                'boring', 'difficult', 'hard', 'challenging', 'poor', 'weak',
                'unpleasant', 'disgusting', 'revolting', 'repulsive', 'offensive',
                'annoying', 'irritating', 'frustrating', 'confusing', 'complicated',
                'messy', 'disorganized', 'chaotic', 'stressful', 'overwhelming',
                'exhausting', 'tiring', 'draining', 'depressing', 'sad', 'unhappy',
                'miserable', 'upset', 'angry', 'furious', 'outraged', 'disgusted',
                'shocked', 'surprised', 'disappointed', 'let-down', 'failed',
                'unsuccessful', 'ineffective', 'useless', 'worthless', 'pointless',
                'meaningless', 'empty', 'hollow', 'shallow', 'superficial',
                'fake', 'artificial', 'forced', 'uncomfortable', 'awkward',
                'embarrassing', 'humiliating', 'shameful', 'regrettable', 'unfortunate',
                'unlucky', 'cursed', 'doomed', 'hopeless', 'impossible', 'unrealistic',
                'unreasonable', 'unfair', 'unjust', 'wrong', 'incorrect', 'false',
                'misleading', 'deceptive', 'dishonest', 'unreliable', 'untrustworthy'
            },
            'neutral': {
                'okay', 'alright', 'fine', 'normal', 'average', 'typical', 'usual',
                'standard', 'regular', 'ordinary', 'common', 'general', 'basic',
                'simple', 'plain', 'moderate', 'medium', 'middle', 'central',
                'balanced', 'neutral', 'stable', 'steady', 'consistent', 'reliable',
                'predictable', 'expected', 'appropriate', 'suitable', 'adequate',
                'sufficient', 'acceptable', 'reasonable', 'logical', 'practical',
                'realistic', 'possible', 'feasible', 'manageable', 'achievable',
                'accessible', 'available', 'present', 'existing', 'current',
                'recent', 'modern', 'contemporary', 'traditional', 'classic',
                'conventional', 'formal', 'informal', 'casual', 'professional'
            }
        }

    def _determine_word_sentiment(self, word, sentiment_dict):
        """Determine sentiment of a word"""
        word_lower = word.lower()
        
        if word_lower in sentiment_dict['positive']:
            return 'positive'
        elif word_lower in sentiment_dict['negative']:
            return 'negative'
        elif word_lower in sentiment_dict['neutral']:
            return 'neutral'
        else:
            # For unknown words, try to infer sentiment from common patterns
            if any(suffix in word_lower for suffix in ['ful', 'ing', 'ed'] if word_lower.endswith(suffix)):
                return 'neutral'
            return 'neutral'

    def _update_sentiment_words_in_database(self, activity_id, sentiment_words):
        """Update sentiment words in database"""
        # Clear existing sentiment words for this activity
        delete_query = "DELETE FROM sentiment_words WHERE activity_id = %s"
        DbConnection.execute_query(delete_query, (activity_id,))
        
        # Insert new sentiment words
        if sentiment_words:
            insert_queries = []
            for word_data in sentiment_words:
                insert_query = """INSERT INTO sentiment_words (activity_id, word, frequency, sentiment_type)
                                 VALUES (%s, %s, %s, %s)"""
                insert_queries.append((insert_query, (activity_id, word_data['word'], 
                                                    word_data['frequency'], word_data['sentiment'])))
            
            # Use transaction for bulk insert
            success, result = DbConnection.execute_transaction(insert_queries)
            if success:
                print(f"Updated {len(sentiment_words)} sentiment words for activity {activity_id}")
            else:
                print(f"Error updating sentiment words: {result}")

    def get_activity_sentiment_summary(self, activity_id):
        """Get sentiment summary for an activity"""
        query = """SELECT sentiment_type, COUNT(*) as word_count, SUM(frequency) as total_frequency
                   FROM sentiment_words 
                   WHERE activity_id = %s
                   GROUP BY sentiment_type"""
        
        success, result = DbConnection.execute_query(query, (activity_id,), fetch_all=True)
        if not success:
            return {}
        
        sentiment_summary = {}
        for sentiment_type, word_count, total_frequency in result:
            sentiment_summary[sentiment_type] = {
                'word_count': word_count,
                'total_frequency': total_frequency
            }
        
        return sentiment_summary

    def get_top_sentiment_words_across_activities(self, sentiment_type='positive', limit=20):
        """Get top sentiment words across all activities"""
        query = """SELECT word, SUM(frequency) as total_frequency, COUNT(DISTINCT activity_id) as activity_count
                   FROM sentiment_words 
                   WHERE sentiment_type = %s
                   GROUP BY word
                   ORDER BY total_frequency DESC, activity_count DESC
                   LIMIT %s"""
        
        success, result = DbConnection.execute_query(query, (sentiment_type, limit), fetch_all=True)
        if success:
            return [{'word': row[0], 'frequency': row[1], 'activity_count': row[2]} for row in result]
        return []

    def analyze_sentiment_trends(self):
        """Analyze sentiment trends across all activities"""
        # Get overall sentiment distribution
        query = """SELECT a.name, a.id,
                          COALESCE(pos.word_count, 0) as positive_words,
                          COALESCE(neg.word_count, 0) as negative_words,
                          COALESCE(neu.word_count, 0) as neutral_words,
                          COALESCE(ar.average_rating, 0) as avg_rating
                   FROM activities a
                   LEFT JOIN activity_ratings ar ON a.id = ar.activity_id
                   LEFT JOIN (
                       SELECT activity_id, COUNT(*) as word_count 
                       FROM sentiment_words 
                       WHERE sentiment_type = 'positive' 
                       GROUP BY activity_id
                   ) pos ON a.id = pos.activity_id
                   LEFT JOIN (
                       SELECT activity_id, COUNT(*) as word_count 
                       FROM sentiment_words 
                       WHERE sentiment_type = 'negative' 
                       GROUP BY activity_id
                   ) neg ON a.id = neg.activity_id
                   LEFT JOIN (
                       SELECT activity_id, COUNT(*) as word_count 
                       FROM sentiment_words 
                       WHERE sentiment_type = 'neutral' 
                       GROUP BY activity_id
                   ) neu ON a.id = neu.activity_id
                   ORDER BY avg_rating DESC"""
        
        success, result = DbConnection.execute_query(query, fetch_all=True)
        if success:
            trends = []
            for row in result:
                activity_name, activity_id, pos_words, neg_words, neu_words, avg_rating = row
                total_words = pos_words + neg_words + neu_words
                
                if total_words > 0:
                    sentiment_score = (pos_words - neg_words) / total_words
                else:
                    sentiment_score = 0
                
                trends.append({
                    'activity_name': activity_name,
                    'activity_id': activity_id,
                    'positive_words': pos_words,
                    'negative_words': neg_words,
                    'neutral_words': neu_words,
                    'total_words': total_words,
                    'sentiment_score': sentiment_score,
                    'average_rating': float(avg_rating) if avg_rating else 0.0
                })
            
            return trends
        return []

    def update_all_activity_sentiment_words(self):
        """Update sentiment words for all activities"""
        # Get all activities
        query = "SELECT id FROM activities"
        success, activities = DbConnection.execute_query(query, fetch_all=True)
        
        if not success:
            print("Error retrieving activities")
            return False
        
        updated_count = 0
        for (activity_id,) in activities:
            try:
                self.extract_and_analyze_sentiment_words(activity_id)
                updated_count += 1
            except Exception as e:
                print(f"Error updating sentiment words for activity {activity_id}: {e}")
        
        print(f"Updated sentiment words for {updated_count} activities")
        return True

    def __str__(self):
        return (f"Statistics [Total Participants={self.get_total_participants()}, "
                f"Most Popular Activity={self.get_most_popular_activity()}, "
                f"Average Participants={self.get_average_participants()}]")