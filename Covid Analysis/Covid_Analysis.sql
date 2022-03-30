Select *
From Covid_Analysis..CovidDeaths
order by 3,4
--Select *
--From Covid_Analysis..CovidVaccination
--order by 3,4
--Select the data will be used
Select location,date,total_cases,new_cases,total_deaths,population
From Covid_Analysis..CovidDeaths
order by 1,2

--Total Cases vs Total Deaths
Select location,date,total_cases,total_deaths,(total_deaths/total_cases)*100 as Death_Percentage
From Covid_Analysis..CovidDeaths
where location like '%vietnam%'
order by 1,2

--Total Cases vs Population
Select location,date,total_cases,population,(total_cases/population)*100 as Infection_Percentage
From Covid_Analysis..CovidDeaths
where location like '%vietnam%'
order by 1,2

--Countries with Highest Infection Rates by Population
Select location,population,max(total_cases) as HighestInfection,max((total_cases/population))*100 as Infection_Percentage
From Covid_Analysis..CovidDeaths
group by location,population
order by 4 desc

--Countries with Highest Death Rates by Population
Select location,max(cast(total_deaths as int)) as TotalDeathCount,max((total_deaths/population))*100 as Death_Percentage
From Covid_Analysis..CovidDeaths
where continent is not null
group by location,population
order by TotalDeathCount desc

--Continent Death Count
Select location,max(cast(total_deaths as int)) as TotalDeathCount
From Covid_Analysis..CovidDeaths
where continent is null
AND not location = 'Upper middle income'
AND not location = 'High income'
AND not location = 'Lower middle income'
AND not location = 'Low income'
group by location
order by TotalDeathCount desc

--Global Numbers
Set Arithabort off
SET ANSI_WARNINGS OFF
Select sum(cast(new_cases as float)) as total_cases, sum(cast(new_deaths as float)) as total_death,
sum(cast(new_deaths as float))/sum(cast(new_cases as float))*100 as death_percentage
From Covid_Analysis..CovidDeaths
where continent is not null
--group by date
order by 1


--Join the 2 tables
--Total population vs vaccination
drop table if exists #Percent_Population_Vaccinated
Create table #Percent_Population_Vaccinated
(
continent varchar(255),
location varchar(255),
date datetime,
population numeric,
new_vaccination numeric,
rolling_people_vaccinated numeric
)
Insert into #Percent_Population_Vaccinated
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
sum(convert(float,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vaccinated
from Covid_Analysis..CovidDeaths dea
join Covid_Analysis..CovidVaccination vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null

Select*,(rolling_people_vaccinated/population)*100
from #Percent_Population_Vaccinated
GO

--Create a View
Create View PercentPopulationVaccinated as
Select dea.continent,dea.location,dea.date,dea.population,vac.new_vaccinations, 
sum(convert(float,vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as rolling_people_vaccinated
from Covid_Analysis..CovidDeaths dea
join Covid_Analysis..CovidVaccination vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
GO

drop view Percent_Population_Vaccinated

