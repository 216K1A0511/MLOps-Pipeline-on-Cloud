"""
Engagement Analytics Dashboard inspired by FinalLayer
"""

import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

class EngagementAnalytics:
    def __init__(self, log_file="linkedin_engagement_logs.json"):
        self.log_file = log_file
    
    def load_logs(self):
        """Load engagement logs from file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            return []
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def generate_report(self):
        """Generate engagement analytics report"""
        logs = self.load_logs()
        
        if not logs:
            print("No engagement data available yet.")
            return
        
        # Create DataFrame
        data = []
        for log in logs:
            entry = {
                'date': log['timestamp'][:10],
                'predicted_impressions': log['predictions']['predicted_impressions'],
                'engagement_score': log['predictions']['engagement_score'],
                'has_question': log['predictions']['content_analysis']['has_question']
            }
            data.append(entry)

        df = pd.DataFrame(data)
        
        # Generate insights
        import sys
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')

        print("\n" + "="*60)
        print("LinkedIn Engagement Analytics Report")
        print("="*60)
        
        print(f"\n📊 Total Posts Analyzed: {len(df)}")
        print(f"📈 Average Predicted Impressions: {df['predicted_impressions'].mean():,.0f}")
        print(f"⭐ Average Engagement Score: {df['engagement_score'].mean():.2f}")
        
        # Best performing factors
        if 'has_question' in df.columns:
            question_posts = df[df['has_question'] == True]
            no_question_posts = df[df['has_question'] == False]
            
            if len(question_posts) > 0 and len(no_question_posts) > 0:
                avg_with_question = question_posts['predicted_impressions'].mean()
                avg_without_question = no_question_posts['predicted_impressions'].mean()
                
                if avg_without_question > 0:
                    improvement = ((avg_with_question - avg_without_question) / avg_without_question) * 100
                    print(f"\n💡 Question in post improves reach by: {improvement:.1f}%")
        
        # Generate visualization
        self._create_visualization(df)
    
    def _create_visualization(self, df):
        """Create visualization of engagement trends"""
        try:
            plt.figure(figsize=(12, 6))
            
            # Plot predicted impressions over time
            plt.subplot(1, 2, 1)
            plt.plot(range(len(df)), df['predicted_impressions'], marker='o', linewidth=2)
            plt.title('Predicted Impressions Trend')
            plt.xlabel('Post Number')
            plt.ylabel('Impressions')
            plt.grid(True, alpha=0.3)
            
            # Plot engagement score
            plt.subplot(1, 2, 2)
            plt.bar(range(len(df)), df['engagement_score'], color='skyblue')
            plt.title('Engagement Score per Post')
            plt.xlabel('Post Number')
            plt.ylabel('Score')
            plt.axhline(y=df['engagement_score'].mean(), color='r', linestyle='--', label=f'Avg: {df["engagement_score"].mean():.2f}')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('engagement_analytics.png', dpi=300, bbox_inches='tight')
            print("\n📈 Analytics visualization saved as 'engagement_analytics.png'")
        except Exception as e:
            print(f"Could not create visualization: {e}")

# Run analytics
if __name__ == "__main__":
    analyzer = EngagementAnalytics()
    analyzer.generate_report()
