import os
import csv
import pandas as pd
import numpy as np
from tabulate import tabulate
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from graphs import show_graphs   # import graph function


def run_menu():
    print("============================================")
    print(" SMART STUDENT ANALYTICS SYSTEM ")
    print("============================================")
    print("1. Add Student ")
    print("2. View All Students")
    print("3. Analyze Performance ")
    print("4. Show Graphs")
    print("5. Export Report")
    print("6. Exit")

    filename = 'student_information.csv'
    headers = [
        'id', 'name', 'Gender', 'Class',
        'math_marks','Chemistry_marks','Physics_marks',
        'Sci_marks','Social_Sci_marks',
        'Eng_marks','Computer_marks','attendence'
    ]

    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    option = int(input("Enter Your Choice: "))

    while True:
        match option:

            case 1:
                print("Enter Student(Details) \n ")
                stu_id=int(input("Enter Student ID: "))
                stu_name=input("Enter Name: ")
                stu_gender=input("Enter your Gender: ")
                stu_Class=input("Enter Class: ")
                print("If Subject Is Not Available Then Enter : -1")
                stu_math_marks=int(input("Enter Math Marks: "))
                stu_Chemistry_marks=int(input("Enter Chemistry Marks: "))
                stu_Physics_marks=int(input("Enter Physics Marks: "))
                stu_Sci_marks=int(input("Enter Science Marks: "))
                stu_SocialSci_marks=int(input("Enter Social-Science Marks: "))
                stu_Eng_marks=int(input("Enter English Marks: "))
                stu_Computer_marks=int(input("Enter Computer Marks: "))
                
                stu_attendence=int(input("Enter Attendance (%): "))
                with open('student_information.csv','a+',newline='') as file:
                    writer=csv.writer(file)

                    writer.writerow([stu_id,stu_name,stu_gender,stu_Class,stu_math_marks,stu_Chemistry_marks,stu_Physics_marks,stu_Sci_marks,stu_SocialSci_marks,stu_Eng_marks,stu_Computer_marks,stu_attendence]) 
                    print("\n✅ Student added successfully! ")
            case 2:
                df=pd.read_csv('student_information.csv')
                if df.empty:
                    print("\n ⚠ No student data available!")
                    break
                df.replace(-1, np.nan, inplace=True)
                print("\n====================================== 📊 Student Details ======================================\n")
                print(tabulate(df,headers='keys',tablefmt='basic',showindex=False))
    
            case 3:
                df=pd.read_csv('student_information.csv')
                print("\n")
                print("====================================== 📊 STUDENT PERFORMANCE ANALYSIS ======================================\n")
                print("============== 🎓 Average Marks per Students: ==============\n")

                df.replace(-1, np.nan, inplace=True)
                df[['name','Class']]=df[['name','Class']].fillna("Unknown")
                df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks','attendence']]=df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks','attendence']].fillna(np.nan)
                df.drop_duplicates(inplace=True)
                df['Avg_marks']=df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks']].mean(axis=1).round(2)
                dff=df[['name','Avg_marks']]
                print(tabulate(dff,headers='keys',tablefmt='basic',showindex=False))

                print("\n=================🎓 Subject Average Marks: =================")
                sub_marks=[df['math_marks'].mean().round(2),
                        df['Chemistry_marks'].mean().round(2),
                        df['Physics_marks'].mean().round(2),
                        df['Sci_marks'].mean().round(2),
                        df['Social_Sci_marks'].mean().round(2),
                        df['Eng_marks'].mean().round(2),
                        df['Computer_marks'].mean().round(2)]
                print(f"\nMaths:  {sub_marks[0]}\nChemistry:  {sub_marks[1]}\nPhysics:  {sub_marks[2]}\nScience:  {sub_marks[3]}\nSocial_Science:  {sub_marks[4]}\nEnglish:  {sub_marks[5]}\nComputer:  {sub_marks[6]}")

                df['percentage']=(df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks']].mean(axis=1)*100/70).round(2)
                df1=df.sort_values(by="percentage",ascending=False)
                df1 = df1.reset_index(drop=True)
                print("\n====================🏆 Top 3 Students: ====================\n")
                dff1=df1[['name','percentage']].head(3)

                print(tabulate(dff1,headers='keys',tablefmt='basic',showindex=False))
                
                scidata=df[df['Sci_marks']<=26]
                mathdata=df[df['math_marks']<=26]
                engdata=df[df['Eng_marks']<=26]
                chemidata=df[df['Chemistry_marks']<=26]
                physdata=df[df['Physics_marks']<=26]
                socdata=df[df['Social_Sci_marks']<=26]
                compdata=df[df['Computer_marks']<=26]

                failsub=["Science","Maths","English","Chemistry","Physics","Social_Sci_marks","Computer"]
                new_df = pd.concat([scidata[['name']],mathdata[['name']],engdata[['name']],chemidata[['name']],physdata[['name']],socdata[['name']],compdata[['name']]],axis=1)

                print("\n=====================🎓 Fail Students: ===================== \n")
                if(new_df.empty):
                    print("Hurray! No Fail Students. 🎉")     
                else:
                    new_df.fillna("--",inplace=True)
                    print(tabulate(new_df,headers=failsub,tablefmt='basic',showindex=False))
                    

            case 4:
                df = pd.read_csv(filename)
                df.replace(-1, np.nan, inplace=True)
                show_graphs(df)  
            case 5:
                
                df = pd.read_csv('student_information.csv') 
                df.replace(-1, np.nan, inplace=True)
                df.to_csv('student_data_cleaned.csv', index=False)

                with open('performance_summary.txt','w') as file:
                    file.write(f"---------PERFORMANCE SUMMARY REPORT--------- \n")
                    file.write(f"Total Students: {df.shape[0]}\n")

                    df['Avg_marks'] = df[['math_marks','Chemistry_marks','Physics_marks','Sci_marks','Social_Sci_marks','Eng_marks','Computer_marks']].mean(axis=1).round(2)

                    df['percentage'] = (df[['math_marks','Chemistry_marks','Physics_marks',
                                        'Sci_marks','Social_Sci_marks',
                                        'Eng_marks','Computer_marks']].mean(axis=1)*100/70).round(2)

                    file.write(f"Class Average: {df['Avg_marks'].mean().round(2)}\n")

                    df.sort_values(by='percentage', inplace=True, ascending=False)
                    file.write(f"Top Student: {df.iloc[0]['name']}\n")

                    nfl = set()
                    failstudent = df.query(
                    'math_marks<26 or Sci_marks<26 or Eng_marks<26 or '
                    'Chemistry_marks<26 or Physics_marks<26 or '
                    'Social_Sci_marks<26 or Computer_marks <26'
                    )

                    for i in range(failstudent.shape[0]):
                        nfl.add(failstudent.iloc[i]['name'])

                    file.write(f"Total Pass Students: {df.shape[0]-len(nfl)}\n")
                    file.write(f"Total Fail Students: {len(nfl)}\n\n")

                    pdf = canvas.Canvas("performance_summary.pdf", pagesize=A4)
                    width, height = A4

                    x = 50
                    y = height - 50

                    pdf.setFont("Helvetica-Bold", 16)
                    pdf.drawString(x, y, "PERFORMANCE SUMMARY REPORT")

                    pdf.setFont("Helvetica", 12)
                    y -= 40
                    pdf.drawString(x, y, f"Total Students: {df.shape[0]}")

                    y -= 20
                    pdf.drawString(x, y, f"Class Average: {df['Avg_marks'].mean().round(2)}")

                    y -= 20
                    pdf.drawString(x, y, f"Top Student: {df.iloc[0]['name']}")

                    y -= 20
                    pdf.drawString(x, y, f"Total Pass Students: {df.shape[0]-len(nfl)}")

                    y -= 20
                    pdf.drawString(x, y, f"Total Fail Students: {len(nfl)}")

                    y -= 30
                    pdf.setFont("Helvetica-Bold", 12)
                    pdf.drawString(x, y, "Fail Students:")

                    pdf.setFont("Helvetica", 11)
                    y -= 20

                    if len(nfl) == 0:
                        pdf.drawString(x, y, "No failed students 🎉")
                    else:
                        for name in nfl:
                            pdf.drawString(x, y, f"- {name}")
                            y -= 15
                            if y < 50:
                                pdf.showPage()
                                pdf.setFont("Helvetica", 11)
                                y = height - 50

                    pdf.save()

                print("✅ TXT & PDF reports generated successfully!")

            case 6:
                print("👋 Thank you for using Smart Student Analytics System!")
                break

            case _:
                print("❌ Invalid Option! Please Try Again.")

        option = int(input("\nEnter Your Choice: "))
