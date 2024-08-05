## Data Dictionary for the project tables:

### ksp_incidents - 4105 records of incident data (2020-June 2024)

| Column Name          | Data Type | Description                  | Notes                       |
|----------------------|-----------|------------------------------|-----------------------------|
| IncidentID           | INT       | Unique identifier for the incident | Primary key                 |
| AgencyORI            | INT       | Agency Originating Identifier |                             |
| AgencyName           | TEXT      | Name of the reporting agency  |                             |
| IncidentStatusDesc   | TEXT      | Description of the incident status |                             |
| County               | TEXT      | Name of the county            |                             |
| RdwyNumber           | TEXT      | Roadway number                |                             |
| Street               | TEXT      | Street name                   |                             |
| RoadwayName          | TEXT      | Name of the roadway           |                             |
| StreetSfx            | TEXT      | Street suffix                 |                             |
| StreetDir            | TEXT      | Street direction              |                             |
| IntersectionRdwy     | TEXT      | Intersection roadway number   |                             |
| IntersectionRdwyName | TEXT      | Name of the intersection roadway |                           |
| BetweenStRdwy1       | TEXT      | Between street roadway 1      |                             |
| BetweenStRdwyName1   | TEXT      | Name of between street roadway 1 |                         |
| BetweenStRdwy2       | TEXT      | Between street roadway 2      |                             |
| BetweenStRdwyName2   | TEXT      | Name of between street roadway 2 |                         |
| Latitude             | REAL      | Latitude of the incident location |                         |
| Longitude            | REAL      | Longitude of the incident location |                        |
| Milepoint            | REAL      | Milepoint of the incident     |                             |
| CollisionDate        | DATE      | Date of the collision         |                             |
| CollisionTime        | TIME      | Time of the collision         |                             |
| UnitsInvolved        | INT       | Number of units involved      |                             |
| MotorVehiclesInvolved| INT       | Number of motor vehicles involved |                      |
| NumberKilled         | INT       | Number of fatalities          |                             |
| NumberInjured        | INT       | Number of injuries            |                             |
| Weather              | TEXT      | Weather conditions at the time of the incident |             |
| RdwyConditionCode    | INT       | Code representing roadway condition |                   |
| HitandRun            | TEXT      | Hit and run indicator         |                             |
| DirAnalysisCode      | TEXT      | Direction analysis code       |                             |
| MannerofCollision    | TEXT      | Manner of collision           |                             |
| RdwyCharacter        | TEXT      | Roadway character             |                             |
| LightCondition       | TEXT      | Light conditions at the time of the incident |               |
| RampFromRdwyId       | TEXT      | Ramp from roadway ID          |                             |
| RampToRdwyId         | TEXT      | Ramp to roadway ID            |                             |
| AcceptedDate         | DATE      | Date when the incident was accepted |                       |
| IsSecondaryCollision | TEXT      | Indicator of secondary collision |                         |
| OwnerBadge           | TEXT      | Owner badge                   |                             |
| IncidentStatus       | TEXT      | Status of the incident        |                             |

### ksp_controls - 13492 records of traffic control devices in place at the time of the incident

| Column Name         | Data Type | Description                  | Notes                       |
|---------------------|-----------|------------------------------|-----------------------------|
| IncidentID          | INT       | Unique identifier for the incident | Foreign key references `ksp_incidents` |
| TrafficControlNo    | INT       | Traffic control number       |                             |
| TrafficControl      | TEXT      | Type of traffic control | 'STOP & GO SIGNAL', 'ADVISORY SPEED SIGN', 'CENTER LINE', 'OTHER', 'WARNING SIGNS', 'MEDIAN', 'STOP SIGN', 'OFFICER OR FLAGMAN', 'NONE', 'SCHOOL ZONE SIGN', 'CURVE SIGN', 'YIELD SIGN', 'NO PASSING ZONE', 'CROSSWALK', 'FLASHING LIGHT', 'RR SIGNS OR SIGNALS', 'TRAFFIC CONTROL DEVICE MISSING', 'ACCELERATIONDECELERATION LANE', 'RR GATES'  |

### ksp_vehicles

| Column Name           | Data Type | Description                  | Notes                       |
|-----------------------|-----------|------------------------------|-----------------------------|
| IncidentID            | INT       | Unique identifier for the incident | Foreign key references `ksp_incidents` |
| UnitNumber            | INT       | Unit number of the vehicle   |                             |
| UnitType              | TEXT      | Type of the unit | 'HIT & RUN/UNKNOWN', 'LT TRUCK(VAN/SPORTS UTILITY/PICKUP)', 'PASSENGER CAR', 'PASSENGER CAR & TRAILER', 'TRUCK-SINGLE UNIT', 'TRUCK TRACTOR & SEMI-TRAILER', 'OTHER', 'BUS', 'SCHOOL BUS', 'TRUCK & TRAILER', 'MOTOR HOME/RECREATIONAL VEHICLE', 'EMERGENCY VEHICLE-NON RESPONSE', 'MOTORCYCLE', 'FARM TRACTOR &/OR FARM EQUIPMENT', 'TRUCK-OTHER COMBINATION', 'OTHER PUBLIC OWNED VEHICLE', 'EMERGENCY VEHICLE-IN RESPONSE', 'TAXICAB', 'MOTOR SCOOTER OR  MOTOR BICYCLE', 'MILITARY VEHICLE', 'GOCART' |
| AirbagSwitchCde       | TEXT      | Airbag switch code           |                             |
| IsCommercialVeh       | TEXT      | Indicator if the vehicle is commercial |                  |
| CrashAvoidCde         | TEXT      | Crash avoidance code         |                             |
| DriverIdentifiedCde   | TEXT      | Driver identified code       |                             |
| EventCollWithFirstCde | TEXT      | First event collision code   |                             |
| EventCollWithSecondCde| TEXT      | Second event collision code  |                             |
| HasFire               | TEXT      | Indicator if the vehicle caught fire |                       |
| PreCollActionCde      | TEXT      | Pre-collision action code    |                             |
| UnderOverrideCde      | TEXT      | Under override code          |                             |
| VehicleIsInsured      | TEXT      | Indicator if the vehicle is insured |                        |
| MakeCde               | TEXT      | Vehicle make code            |                             |
| ModelCde              | TEXT      | Vehicle model code           |                             |
| VehicleType           | TEXT      | Type of the vehicle          |                             |
| MakeDescription       | TEXT      | Description of the vehicle make |                         |
| ModelDescription      | TEXT      | Description of the vehicle model |                        |

### ksp_person - 15328 records for each person involved in the incidents

| Column Name             | Data Type | Description                  | Notes                       |
|-------------------------|-----------|------------------------------|-----------------------------|
| IncidentID              | INT       | Unique identifier for the incident | Foreign key references `ksp_incidents` |
| UnitNumber              | INT       | Unit number of the vehicle   |                             |
| PersonNo                | INT       | Person number                |                             |
| PersonTypeCde | TEXT | Person type code | '1 - Driver', '2 - Passenger', '3 - Pedestrian', '4 - Animal Drawn/Ridden', '5 - Bicyclist', '6 - Train Engineer', '7 - Witness' ,'8 - Owner' |
| DeathDte                | DATE      | Date of death                |                             |
| AgeAtIncident           | INT       | Age at the time of the incident |                         |
| Gender                  | TEXT      | Gender of the person         |                             |
| IsOwner                 | TEXT      | Indicator if the person is the owner |                    |
| WasTransported          | TEXT      | Indicator if the person was transported |                  |
| InjurySeverityCde       | TEXT      | Injury severity code         |                             |
| InjuryLocationCde       | TEXT      | Injury location code         |                             |
| PosInVehicleCde         | TEXT      | Position in vehicle code     |                             |
| RestraintUseCde         | TEXT      | Restraint use code           |                             |
| TrappedCde              | TEXT      | Indicator if the person was trapped |                       |
| EjectionCde             | TEXT      | Ejection code                |                             |
| EjectionPathCde         | TEXT      | Ejection path code           |                             |
| SuspectedOfDrinking     | TEXT      | Indicator if the person was suspected of drinking |          |
| TestOffered             | TEXT      | Indicator if the person was offered a test |              |
| TestRefused             | TEXT      | Indicator if the person refused the test |               |
| TestedForCde            | TEXT      | Code of the test conducted   |                             |
| TestSentTo              | TEXT      | Location where the test was sent |                         |
| TestResults             | TEXT      | Results of the test          |                             |
| HasOpLicense            | TEXT      | Indicator if the person has an operator license |           |
| HasCDLicense            | TEXT      | Indicator if the person has a commercial driver license |   |
| HasLicenseRestrictions  | TEXT      | Indicator if the person has license restrictions |         |
| HasOpEndorsements       | TEXT      | Indicator if the person has operator endorsements |         |

### ksp_factors

| Column Name | Data Type | Description                  | Notes                       |
|-------------|-----------|------------------------------|-----------------------------|
| IncidentID  | INT       | Unique identifier for the incident | Foreign key references `ksp_incidents` |
| UnitNumber  | INT       | Unit number of the vehicle   |                             |
| Factor_Type | TEXT      | Type of the factor | 'ENVIRON FACTOR', 'HUMAN FACTOR', 'VEHICULAR FACTOR', 'DRIVER DISTRACTED BY |
| Factor      | TEXT      | Description of the factor    |                             |

### county_district_lut

| Column Name          | Data Type | Description                  | Notes                       |
|----------------------|-----------|------------------------------|-----------------------------|
| OBJECTID             | INT       | Unique identifier for the record |                          |
| Cnty_Name_UC         | TEXT      | County name in uppercase     |                             |
| Cnty_Name_PC         | TEXT      | County name in proper case   |                             |
| Cnty_Number          | INT       | County number                |                             |
| Cnty_FIPS_Number     | INT       | FIPS number of the county    |                             |
| KYTC_District_Number | INT       | KYTC district number         |                             |
| D_DISTRICT  | TEXT | District name       | Name of the City of District Office Location |

### unit_factor_code_lut

| Column Name | Data Type | Description                  | Notes                       |
|-------------|-----------|------------------------------|-----------------------------|
| Factor_code | TEXT      | Code representing the factor |  1 - 99 |
| Description | TEXT      | Description of the factor    | '1 - Alcohol Involvement', '2 - Cell Phone', '3 - Disregard Traffic Control', '4 - Distraction', '5 - Drug Involvement', '6 - Emotional', '7 - Exceeded Stated Speed Limit', '8 - Failed to Yield Right of Way', '9 - Fatigue', '10 - Fell Asleep', '11 - Following Too Close', '12 - Improper Backing', '13 - Improper Passing', '14 - Inattention', '15 - Lost Consciousness/Fainted', '16 - Medication', '17 - Misjudge Clearance', '18 - Not Under Proper Control', '19 - Overcorrecting/Oversteering', '20 - Physical Disability', '21 - Sick', '22 - Too Fast for Conditions', '23 - Turning Improperly', '24 - Weaving in Traffic', '97 - Other', '99 - None Detected' |

### roadway_characteristics_api

| Column Name               | Data Type | Description                  | Notes                       |
|---------------------------|-----------|------------------------------|-----------------------------|
| Cardinality | TEXT | Cardinal direction of the roadway | 'Cardinal', 'Non-Cardinal'|
| County_Name | TEXT | Name of the county | |
| Direction | TEXT | Direction of the roadway | 'Northbound', 'Southbound', 'Northbound & Southbound', 'Eastbound', 'Westbound', 'None', 'Eastbound & Westbound'|
| Government_Level | TEXT | Agency responsibile for road maintenance | 'State Maintained Roads', 'City Maintained Roads', 'County Maintained Roads', 'Private Roads', 'Other State Agency Roads', 'Route belongs to adjacent state' |
| Grade_Percent | FLOAT | Percentage of the Grade of the Route Section | |
| Lane_Width_Feet | FLOAT | Width of the Lane | |
| Median_Type | TEXT | | 'Depressed', 'Other Positive Barrier','None', 'Guardrail Barrier', 'Concrete Barrier', 'Raised Non Mountable', 'Flush', 'Raised Mountable' |
| Median_Width_Feet | FLOAT | Width of the Median, if present | |
| Road_Name | TEXT | Official Name of the Road | |
| Route | TEXT | Route Label | |
| Route_Type | TEXT || 'I - Interstate', 'PKWY - Parkway', 'US - US Route', "KY - State Route' |
| Route_Unique_Identifier | TEXT | KYTC designated unique identifier for specific route section | |
| Milepoint | NUMERIC | Distance along the route assigned from county boundary entrance to county boundary exit  | |
| Speed_Limit_Posted_MPH | INT | Officially Posted speed limit | |
| Traffic_Last_Count | INT | Average annual daily traffic count | |
| Truck_Weight_Limit_Class | TEXT | Weight Class assigned to the roadway section | '80 000 lbs maximum', '62 000 lbs maximum', 'None', '44 000 lbs maximum' |
| Type_Operation | TEXT | Indicates travel along the roadway |'One Side of Divided Highway', 'Two-Way', 'One-Way' |
| Geometry | TEXT | Spatial data that represents the shape and location of physical features on the earth’s surface | |
| IncidentID | INT | Unique identifier for the incident | Foreign key references `ksp_incidents` |