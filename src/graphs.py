import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def show_graphs(df):

    df=pd.read_csv('student_information.csv')
    df.replace(-1, np.nan, inplace=True)
    plt.style.use('seaborn-v0_8')

    fig, ax = plt.subplots(2, 2,figsize=(10, 8),constrained_layout=True)

    subjects =['Maths','Science','English','Chemistry','Physics','Social_Sci','Computer']
    avg_marks = [
    df['math_marks'].mean(),
    df['Sci_marks'].mean(),
    df['Eng_marks'].mean(),
    df['Chemistry_marks'].mean(),
    df['Physics_marks'].mean(),
    df['Social_Sci_marks'].mean(),
    df['Computer_marks'].mean()
    ]

    ax[0, 0].bar(subjects, avg_marks, color='orange', edgecolor='black')
    ax[0, 0].set_xlabel('Subject')
    ax[0, 0].set_ylabel('Average Marks')
    ax[0, 0].set_title('Subject wise Average Marks')
    ax[0, 0].grid(axis='y', linestyle='--', alpha=0.6)

    for i, v in enumerate(avg_marks):
        ax[0, 0].text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')


    failstu = df.query('math_marks <= 26 or Sci_marks <= 26 or Eng_marks <= 26 or Chemistry_marks <=26 or Physics_marks <=26 or Social_Sci_marks <=26 or Computer_marks <=26')

    ax[0, 1].pie(
    [failstu.shape[0], df.shape[0] - failstu.shape[0]],
    labels=['Fail', 'Pass'],
    autopct='%1.1f%%',
    startangle=90,
    shadow=True
    )
    ax[0, 1].set_title('Percentage of Pass / Fail Students')
    ax[0, 1].axis('equal')


    df['newpercentage'] = df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks']].mean(axis=1) * 100/70
    df['Gender'] = df['Gender'].str.capitalize()
    df11=df[df['Gender']=="Male"]
    df22=df[df['Gender']=="Female"]
    ax[1, 0].scatter(df11['attendence'],df11['newpercentage'],color='red',marker='o',linewidth=2,label='Male')
    ax[1, 0].scatter(df22['attendence'],df22['newpercentage'],color='green',marker='o',linewidth=2,label='Female' )
    ax[1, 0].set_xlabel('Attendance')
    ax[1, 0].set_ylabel('Percentage')
    ax[1, 0].set_title('Attendance vs Percentage')
    ax[1, 0].grid(True, linestyle='--', alpha=0.6)
    ax[1, 0].legend()
    subject_cols = [
    'math_marks','Chemistry_marks','Physics_marks',
    'Sci_marks','Social_Sci_marks',
    'Eng_marks','Computer_marks'
    ]
    yticklabels = df['id']

    sns.heatmap(
    df[subject_cols],
    annot=True,
    cmap='YlGnBu',
    linewidths=0.5,
    yticklabels=yticklabels.tolist(),
    ax=ax[1,1],
    cbar=False
    )
    ax[1,1].set_xticklabels(['Maths','Chemistry','Physics','Science','Social Science','English','Computer'], rotation=0,ha='center')
    ax[1,1].set_yticklabels(df['id'].astype(str).tolist(),rotation=0,va='center')
    ax[1,1].set_xlabel('Subjects')
    ax[1,1].set_title('Student-wise Subject Marks')
    ax[1,1].set_ylabel('Student ID')
    fig.suptitle('Student Performance Analytics Dashboard', fontsize=18, fontweight='bold')
    plt.show()    
    