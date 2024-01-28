drop table if exists #t1
select * into #t1 from dw.fnGetFactS1CourseEnrolments(getdate(),-1)

select * into #t2 from dw.vwFactCourseExits

select 
--a.keyStudent,a.keyFacultyOpsS1,
IsExit=case when b.keyStudent is not null then 1 else 0 end
,ExitReason=b.WD_Withdrawn_Reason 
,IsTDP=case a.[TDP or Non - TDP] when 'TDP' then 1 else 0 end
,LiabilityCode=a.[Liability Code]
,TotalHours=a.Total_Hours
,CourseMode=a.[Course Study Mode Description]

--Student
,HighEdu=se.Code
,CoB=s.COB
,s.CALD

--Course
,c.FacultyCode
,c.DeptCode

from #t1 a 
outer apply
(
select top 1 * from #t2 where #t2.keyStudent=a.keyStudent and #t2.keyFacultyOpsS1=a.keyFacultyOpsS1
order by #t2.CRDATEI desc
) b
inner join dw.DimStudent s on s.keyStudent=a.keyStudent
left join dw.vwfactStudentEducation se on s.Student_Id=se.STU_ID and se.Is_Highest_Edu=1
inner join dw.DimFacultyOpsS1 c on c.keyFacultyOpsS1=a.keyFacultyOpsS1 and c.CourseTypeName not in ('Short Course')


select * from #t1
select * from #t2


select b.keyStudent,b.keyFacultyOpsS1,count(10) from #t2 b group by b.keyStudent,b.keyFacultyOpsS1 having count(1)>1

select * from dw.DimFacultyOpsS1