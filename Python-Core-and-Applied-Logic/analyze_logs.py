import pandas as pd
import sys
from datetime import datetime

def validate_duration(duration):
    """Validate and clean duration values"""
    try:
        duration = float(duration)
        if duration < 0:
            return None
        return duration
    except (ValueError, TypeError):
        return None

def validate_timestamp(timestamp):
    """Validate timestamp format"""
    try:
        datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def analyze_logs(input_file='task_logs.csv', output_file='summary_report.csv'):
    """
    Analyze task logs and generate summary metrics
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output summary CSV file
    """
    try:
        # Read CSV file
        df = pd.read_csv(input_file)
        
        print("=" * 60)
        print("TASK LOG ANALYSIS REPORT")
        print("=" * 60)
        print(f"\nTotal records loaded: {len(df)}")
        
        # Data validation
        original_count = len(df)
        
        # Validate timestamps
        df['valid_timestamp'] = df['start'].apply(validate_timestamp)
        invalid_timestamps = df[~df['valid_timestamp']]
        if len(invalid_timestamps) > 0:
            print(f"\n⚠ Warning: {len(invalid_timestamps)} invalid timestamps found:")
            print(invalid_timestamps[['user', 'task_type', 'start']])
        
        # Clean and validate durations
        df['duration_clean'] = df['duration_min'].apply(validate_duration)
        invalid_durations = df[df['duration_clean'].isna() & df['duration_min'].notna()]
        if len(invalid_durations) > 0:
            print(f"\n⚠ Warning: {len(invalid_durations)} invalid durations found:")
            print(invalid_durations[['user', 'task_type', 'duration_min']])
        
        # Remove invalid records
        df_clean = df[df['valid_timestamp'] & df['duration_clean'].notna()].copy()
        df_clean['duration_min'] = df_clean['duration_clean']
        
        removed_count = original_count - len(df_clean)
        if removed_count > 0:
            print(f"\n✓ Removed {removed_count} invalid records")
        print(f"✓ Valid records for analysis: {len(df_clean)}")
        
        # 1. Total time per user
        print("\n" + "=" * 60)
        print("1. TOTAL TIME PER USER")
        print("=" * 60)
        time_per_user = df_clean.groupby('user')['duration_min'].agg([
            ('total_minutes', 'sum'),
            ('total_hours', lambda x: round(x.sum() / 60, 2)),
            ('task_count', 'count')
        ]).reset_index()
        time_per_user = time_per_user.sort_values('total_minutes', ascending=False)
        print(time_per_user.to_string(index=False))
        
        # 2. Total time per task type
        print("\n" + "=" * 60)
        print("2. TOTAL TIME PER TASK TYPE")
        print("=" * 60)
        time_per_task = df_clean.groupby('task_type')['duration_min'].agg([
            ('total_minutes', 'sum'),
            ('total_hours', lambda x: round(x.sum() / 60, 2)),
            ('task_count', 'count'),
            ('avg_duration', lambda x: round(x.mean(), 2))
        ]).reset_index()
        time_per_task = time_per_task.sort_values('total_minutes', ascending=False)
        print(time_per_task.to_string(index=False))
        
        # 3. Top 3 task types by total time
        print("\n" + "=" * 60)
        print("3. TOP 3 TASK TYPES BY TOTAL TIME")
        print("=" * 60)
        top_3_tasks = time_per_task.head(3)
        for idx, row in top_3_tasks.iterrows():
            print(f"{idx + 1}. {row['task_type']}: {row['total_minutes']} minutes ({row['total_hours']} hours)")
        
        # 4. User-Task breakdown
        print("\n" + "=" * 60)
        print("4. USER-TASK TYPE BREAKDOWN")
        print("=" * 60)
        user_task_breakdown = df_clean.groupby(['user', 'task_type'])['duration_min'].agg([
            ('total_minutes', 'sum'),
            ('task_count', 'count')
        ]).reset_index()
        user_task_breakdown = user_task_breakdown.sort_values(['user', 'total_minutes'], ascending=[True, False])
        print(user_task_breakdown.to_string(index=False))
        
        # Save summary report
        summary_data = []
        
        # Add user summaries
        for _, row in time_per_user.iterrows():
            summary_data.append({
                'category': 'User',
                'name': row['user'],
                'total_minutes': row['total_minutes'],
                'total_hours': row['total_hours'],
                'task_count': row['task_count']
            })
        
        # Add task type summaries
        for _, row in time_per_task.iterrows():
            summary_data.append({
                'category': 'Task Type',
                'name': row['task_type'],
                'total_minutes': row['total_minutes'],
                'total_hours': row['total_hours'],
                'task_count': row['task_count']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(output_file, index=False)
        
        print(f"\n" + "=" * 60)
        print(f"✓ Summary report saved to: {output_file}")
        print("=" * 60)
        
        return df_clean, time_per_user, time_per_task, top_3_tasks
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    analyze_logs()