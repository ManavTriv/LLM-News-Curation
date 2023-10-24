import pymysql
import time
from datetime import datetime
from enum import Enum
import argparse
import os
import subprocess
from threading import *


ENDPOINT = "newscuration-2.c97gf2vuuvlf.us-east-1.rds.amazonaws.com"
USER = "admin"
PWD = "password"
DB = "newscuration"
PORT = 3306
CHARSET = "utf8mb4"


class messageStatus(Enum):
    FAIL = (0,)
    WARN = (1,)
    SUCCESS = 2


class table:
    """
    The generic class object used to initalise a new record in the database
    """

    tableName = ""

    def __init__(self):
        self.isInserted = False
        self.id = None
        self.name = None

    def insertSQL(self, insertedBy):
        pass

    def querySQL(self):
        return self.isInserted

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name


class Article(table):
    """
    FIELDS:
    ID INT AUTO_INCREMENT PRIMARY KEY,
    URL VARCHAR(255), -- Adjust the length as needed for your URLs
    UpperBias DECIMAL(5, 2), -- 5 total digits with 2 decimal places
    LowerBias DECIMAL(5, 2), -- lower bias score
    Summary TEXT, -- TEXT type allows up to 65,535 characters
    Views INT,
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50)
    """

    def __init__(
        self,
        url: str,
        header: str,
        originalText: str,
        summaryParagraph: str,
        upperBias: float,
        lowerBias: float,
        inProduction: bool,
    ):
        super().__init__()
        self.url = url
        self.upperBias = upperBias
        self.lowerBias = lowerBias
        self.inProd = inProduction
        self.header = header
        self.originalText = originalText
        self.summaryParagraph = summaryParagraph
        Article.tableName = Article.__name__

    def __str__(self):
        if self.id is None:
            return (
                f"{Article.tableName} Record has not been inserted into DB - ID is NONE"
            )
        else:
            return f"{Article.tableName}[{self.id}, {self.url}, {self.upperBias}, {self.lowerBias}, {self.inProd}, {self.header}, {self.originalText}, {self.summaryParagraph}]"

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {Article.tableName} (URL, upperBias, lowerBias, InProduction, InsertedAt, InsertedBy, Header, OriginalText, SummaryParagraph, Views)
        VALUES (
        '{self.url}',
        {self.upperBias},
        {self.lowerBias},
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}',
        '{self.header}',
        '{self.originalText}',
        '{self.summaryParagraph}',
        1
        );
        """
        return query

    def getName(self):
        return Article.tableName


class Politician_PositionNameCodes(table):
    """
    ID
    NameCode VARCHAR(255) NOT NULL UNIQUE,
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50)
    """

    def __init__(self, nameCode=str, inProduction=bool):
        super().__init__()
        self.nameCode = nameCode
        self.inProd = inProduction
        self.name = Politician_PositionNameCodes.__name__

    def __str__(self):
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.nameCode}, {self.inProd}]"

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name} (NameCode, InProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.nameCode}',
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query

    def getName(self):
        return self.name


class Politician(table):
    """
    ID
    Fname VARCHAR(255),
    Lname VARCHAR(255),
    About VARCHAR(1500),
    Age INT,
    Gender VARCHAR(255),
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50)
    """

    def __init__(
        self,
        fName=str,
        lName=str,
        about=str,
        age=int,
        gender=str,
        inProduction=bool,
        imageLink=str,
        summary=str,
        byline=str,
        politicialPosition=str,
        party=str,
        countryCode="AUS",
    ):
        super().__init__()
        self.fName = fName
        self.lName = lName
        self.about = about
        self.age = age
        self.gender = gender
        self.inProd = inProduction
        self.summary = summary
        self.imageLink = imageLink
        self.byline = byline
        self.politicalPosition = politicialPosition
        self.party = party
        self.countryCode = countryCode
        self.name = Politician.__name__

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter;
        the name of the user inserting the record.
        """
        query = f"""
    INSERT INTO {self.name} (Fname, Lname, About, Age, Gender, InProduction, InsertedAt, InsertedBy, ImageLink, Summary, Byline, Political_Position, Party, CountryCode)
    VALUES (
    '{self.fName}',
    '{self.lName}',
    '{self.about}',
    '{self.age}',
    '{self.gender}',
    {1 if self.inProd else 0}, 
    NOW(),
    '{insertedBy}',
    '{self.imageLink}',
    '{self.summary}',
    '{self.byline}',
    '{self.politicalPosition}',
    '{self.party}',
    '{self.countryCode}'
    );
    """
        return query

    def __str__(self):
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.fName}, {self.lName}, {self.about}, {self.age}, {self.gender}, {self.inProd}, {self.imageLink}, {self.summary}]"


class Politician_CampaignPolicies(table):
    """
    ID
    PositionNameCode VARCHAR(255),
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50),
    """

    def __init__(
        self, Fname=str, Lname=str, policyTitle=str, policyInfo=str, inProd=bool
    ):
        super().__init__()
        self.fname = Fname
        self.lname = Lname
        self.policyTitle = policyTitle
        self.policyInfo = policyInfo
        self.inProd = inProd
        self.name = Politician_CampaignPolicies.__name__

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(Fname, Lname, PolicyNameTitle, PolicyInfo, InProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.fname}',
        '{self.lname}',
        '{self.policyTitle}',
        '{self.policyInfo}',
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query

    def __str__(self):
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.fname}, {self.lname}, {self.policyTitle}, {self.policyInfo}, {self.inProd}]"


class Politician_CampaignPoliciesByID(table):
    def __init__(self, ID_Politician, policyTitle=str, policyInfo=str, inProd=bool):
        super().__init__()
        self.ID_Politician = ID_Politician
        self.policyTitle = policyTitle
        self.policyInfo = policyInfo
        self.inProd = inProd
        self.name = Politician_CampaignPoliciesByID.__name__

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
    INSERT INTO {self.name}(Fname, Lname, PolicyNameTitle, PolicyInfo, InProduction, InsertedAt, InsertedBy)
    VALUES (
    '{self.ID_Politician}',
    '{self.policyTitle}',
    '{self.policyInfo}',
    {1 if self.inProd else 0}, 
    NOW(),
    '{insertedBy}'
    );
    """
        return query

    def __str__(self):
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.ID_Politician}, {self.policyTitle}, {self.policyInfo}, {self.inProd}]"


class Politician_Position(table):
    """
    ID
    PositionNameCode VARCHAR(255),
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50),
    """

    def __init__(self, positionNameCode=str, inProduction=bool):
        super().__init__()
        self.posNameCode = positionNameCode
        self.inProd = inProduction
        self.name = Politician_Position.__name__

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(PositionNameCode, InProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.posNameCode}',
        {1 if self.inProd else 0},
        NOW(),
        '{insertedBy}'
        );
        """
        return query

    def __str__(self):
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.posNameCode}, {self.inProd}]"


class Politician_KeyTable(table):
    """
    ID
    ID_Politician INT,
    ID_Article INT,
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50),
    """

    def __init__(self, politicianID=str, articleID=str, inProduction=bool):
        super().__init__()
        self.politicianID = politicianID
        self.articleID = articleID
        self.inProd = inProduction
        self.name = Politician_KeyTable.__name__

    def __str__(self):
        if self.id is None:
            return f"{self.name} record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.politicianID}, {self.articleID}, {self.inProd}]"

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(ID_Politician, ID_Article, InProduction, InsertedAt, InsertedBy)
        VALUES (
        {self.politicianID},
        {self.articleID},
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query


class Polling(table):
    """
    ID,
    ID_Article INT,
    Question TEXT,
    OptionFirst TEXT,
    OptionSecond TEXT,
    OptionThird TEXT,
    OptionFourth TEXT,
    VotesFirst INT,
    VotesSecond INT,
    VotesThird INT,
    VotesFourth INT,
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50),
    """

    def __init__(
        self,
        articleID=str,
        question=str,
        optionFirst=str,
        optionSecond=str,
        optionThird=str,
        optionFourth=str,
        inProduction=bool,
    ):
        super().__init__()
        self.articleID = articleID
        self.question = question
        self.optionFirst = optionFirst
        self.optionSecond = optionSecond
        self.optionThird = optionThird
        self.optionFourth = optionFourth
        self.votesFirst = 0
        self.votesSecond = 0
        self.votesThird = 0
        self.votesFourth = 0
        self.inProd = inProduction
        self.name = Polling.__name__

    def __str__(self) -> str:
        if self.id is None:
            return f"{self.name} Record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.articleID} {self.question}, {self.optionFirst}, {self.optionSecond}, {self.optionThird}, {self.optionFourth}, {self.votesFirst}, {self.votesSecond}, {self.votesThird}, {self.votesFourth}, {self.inProd}]"

    def insertSQL(self, insertedBy):
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(ID_Article, Question, OptionFirst, OptionSecond, OptionThird, OptionFourth, VotesFirst, VotesSecond, VotesThird, VotesFourth, inProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.articleID}',
        '{self.question}',
        '{self.optionFirst}',
        '{self.optionSecond}',
        '{self.optionThird}',
        '{self.optionFourth}',
        '{self.votesFirst}',
        '{self.votesSecond}',
        '{self.votesThird}',
        '{self.votesFourth}',
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query

    def getName(self):
        return self.name


class Article_ArticleBias(table):
    """
    ID INT
    KeyPhrase VARCHAR(1000),
    BiasReason TEXT,
    ID_Article INT,
    InProduction BOOLEAN,
    InsertedAt DATETIME,
    InsertedBy VARCHAR(50),
    """

    def __init__(
        self, ID_Article=int, keyPhrase=str, biasReason=bool, inProduction=bool
    ):
        super().__init__()
        self.ID_Article = ID_Article
        self.keyPhrase = keyPhrase
        self.biasReason = biasReason
        self.inProd = inProduction
        self.name = Article_ArticleBias.__name__

    def __str__(self):
        if self.id is None:
            return f"{self.name} record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.ID_Article}, {self.keyPhrase}, {self.biasReason}, {self.inProd}]"

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(KeyPhrase, BiasReason, ID_Article, InProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.keyPhrase}',
        '{self.biasReason}',
        {self.ID_Article},
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query


class Comments(table):
    def __init__(self, url=str, Author=str, Comment=bool, inProduction=bool):
        super().__init__()
        self.url = url
        self.Author = Author
        self.Comment = Comment
        self.inProd = inProduction
        self.name = Comments.__name__

    def __str__(self):
        if self.id is None:
            return f"{self.name} record has not been inserted into DB - ID is NONE"
        else:
            return f"{self.name}[{self.id}, {self.url}, {self.Author}, {self.Comment}, {self.inProd}]"

    def insertSQL(self, insertedBy) -> str:
        """
        This insert statement only takes one parameter; the name of the user inserting the record.
        """
        query = f"""
        INSERT INTO {self.name}(URL, Author, Comment, InProduction, InsertedAt, InsertedBy)
        VALUES (
        '{self.url}',
        '{self.Author}',
        '{self.Comment}',
        {1 if self.inProd else 0}, 
        NOW(),
        '{insertedBy}'
        );
        """
        return query


class transactionDataClient:
    """
    The transactionDataClient. Communicates with the AWS RDS.

    On initialisation, the TDC establishes connections with the database. The TDC
    has functionality to query, perform table updates and query from a sql file under directory "/sql".
    This should only opened once per session
    """

    def __init__(self):
        self.cursor = None
        self.cnx = None
        self.user = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True
        ).stdout.strip()
        if self.user is None:
            self.user = "Guest user (probably Darren)"
        self.cursor, self.cnx = self.establishConnection()

        self.lock = Lock()

    def logMessage(self, status=messageStatus, message=str):
        """
        Builds a log message in the audit file, for safekeeping
        """
        red_text = "\033[91m"
        default_colour = "\033[0m"

        with open("inf/audit/logs.txt", "a") as auditLog:
            message = f"[{datetime.now()}] [{self.user}] [{status.name}] [{message}]"
            auditLog.write(message + "\n")
            if status == messageStatus.FAIL:
                print(f"{red_text}{message}{default_colour}")
            elif status == messageStatus.WARN:
                print(f"{red_text}{message}{default_colour}")
            else:
                print(message)

    def establishConnection(self):
        """
        Establishes connections with the AWS RDS server.

            Returns:
            Cursor -> cursor object for DB DDL.
        """
        if self.cursor is not None or self.cnx is not None:
            self.logMessage(
                messageStatus.WARN, f"Connection and cursor already established."
            )

        # Create a cursor object
        cnx = pymysql.connect(
            host=ENDPOINT,
            user=USER,
            password=PWD,
            charset=CHARSET,
            cursorclass=pymysql.cursors.DictCursor,
            port=PORT,
        )
        self.logMessage(messageStatus.SUCCESS, f"Established connection {cnx}")
        cursor = cnx.cursor()
        self.logMessage(messageStatus.SUCCESS, f"Established cursor {cursor}")
        cursor.execute(f"USE {DB}")
        cnx.commit()
        self.logMessage(
            messageStatus.SUCCESS, f"Established connection to database {DB}"
        )
        return cursor, cnx

    def closeConnection(self):
        self.logMessage(messageStatus.SUCCESS, f"Closing Connection {self.cnx}")
        self.logMessage(messageStatus.SUCCESS, f"Closing cursor {self.cursor}")
        self.cursor.close()
        self.cnx.close()
        self.cursor = None
        self.cnx = None

    def retrieveCursorOutput(self):
        """
        Retrieves the cursor output for the query. Will not return any output for a DDL, for example.
        Selection queries will return an output.
        """
        try:
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"Unable to retrieve results from cursor {e}"
            )

    def generateFromSqlFile(self, sqlFileName=str, import_loc=str):
        """
        Perform database creation from a sql file. This should be used as a once-off, and not for transactional
        database DDL. For example, creating a new table to host all the politicians.
        NOTE: looks in the /sql directory (give the file name only)
        """
        try:
            with open(f"inf/{import_loc}/{sqlFileName}", "r") as sql:
                sqlIn = sql.read()
        except FileNotFoundError:
            self.logMessage(
                messageStatus.FAIL, f"Unable to find file path: {sqlFileName}"
            )
            self.closeConnection()
            exit(1)
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL,
                f"an exception occured in the execution statement: \n {e}",
            )
            self.closeConnection()
        try:
            self.cnx.ping()
            self.cursor.execute(sqlIn)
        except (
            Exception
        ) as e:  # error handling is vague, have to assume basket case here
            self.logMessage(
                messageStatus.FAIL, f"Unable to execute sql \n {sqlIn} with error {e}"
            )
        self.cnx.commit()
        self.logMessage(messageStatus.SUCCESS, f"{sqlIn}")
        return self.retrieveCursorOutput()

    def query(self, table, filter=None):
        """
        Queries a given table, and applies a filter if given
        """
        self.lock.acquire()
        if self.cursor is None:
            self.logMessage(messageStatus.WARN, "Connection is closed. Query failed")

        query = f"""
        SELECT * 
        FROM {table}
        WHERE {filter if filter is not None else '1=1'}
        """
        try:
            self.cnx.ping()
            self.logMessage(messageStatus.SUCCESS, f"Pinging connection")
            self.cursor.execute(query)
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"error building sql statement with error {e}"
            )

        try:
            self.cnx.commit()
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"failed to commit query \n {sql} \n reason: {e}"
            )
        self.logMessage(messageStatus.SUCCESS, f"Successfully attempted query: {query}")

        tmp = self.retrieveCursorOutput()
        self.lock.release()
        return tmp

    def query_special(self, query=str):
        """
        Queries a given table, and applies a filter if given
        """
        self.lock.acquire()
        if self.cursor is None:
            self.logMessage(messageStatus.WARN, "Connection is closed. Query failed")

        try:
            self.cnx.ping()
            self.logMessage(messageStatus.SUCCESS, f"Pinging connection")
            self.cursor.execute(query)
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"error building sql statement with error {e}"
            )

        try:
            self.cnx.commit()
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"failed to commit query \n {sql} \n reason: {e}"
            )

        tmp = self.retrieveCursorOutput()
        self.lock.release()
        return tmp

    def insert(self, table=type(table)):
        self.lock.acquire()
        if self.cursor is None:
            self.logMessage(messageStatus.WARN, "Connection is closed. Query failed")

        DDLMethod = table.insertSQL(self.user)

        try:
            self.cnx.ping()
            self.logMessage(messageStatus.SUCCESS, f"Pinging connection")
            self.cursor.execute(DDLMethod)
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL,
                f"error parsing SQL statement {DDLMethod}: \n error {e}",
            )

        try:
            self.cnx.commit()
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL,
                f"failed to commit query \n {DDLMethod} \n reason: {e}",
            )
        self.logMessage(
            messageStatus.SUCCESS, f"Successfully attempted query: {DDLMethod}"
        )

        # next, find the id of the newly inserted tuple and update the object
        id = self.get_id(table)
        table.setId(id)
        self.lock.release()

    def get_id(self, table=type(table)):
        """
        Retrieve the id that has automatically been generated for an inserted record
        """
        query = f"""
        SELECT MAX(ID) AS ID FROM {table.getName()};
        """
        try:
            self.cnx.ping()
            self.logMessage(messageStatus.SUCCESS, f"Pinging connection")
            self.cursor.execute(query)
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"error parsing SQL statement {query}: \n error {e}"
            )
        try:
            self.cnx.commit()
        except Exception as e:
            self.logMessage(
                messageStatus.FAIL, f"failed to commit query \n {query} \n reason: {e}"
            )
        self.logMessage(messageStatus.SUCCESS, f"Sucessfully transacted query: {query}")

        try:
            out = self.retrieveCursorOutput()
            return out[0]["ID"]
        except IndexError as e:
            self.logMessage(
                messageStatus.FAIL,
                f"failed to properly insert record. Check table name exists and/or is correct.",
            )
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="transaction client handler")

    parser.add_argument(
        "--query", type=str, nargs="+", help="query a table, with no applied filters"
    )

    parser.add_argument(
        "--DDLFromFile",
        type=str,
        nargs="+",
        help="a list a filenames to perform custom DDL or database intialisation",
    )

    parser.add_argument("--debugDDL", action="store_true", help="debug an insert DDL")

    parser.add_argument(
        "--buildDB", action="store_true", help="build all the databases"
    )

    parser.add_argument(
        "--customImport",
        type=str,
        nargs="+",
        help="perform a custom query from the import-custom directory",
    )
    
    parser.add_argument(
        "--DELETEALL",
        action="store_true",
        help="delete all records from the database",
    )

    args = parser.parse_args()

    if args.DDLFromFile is not None:
        print(f"performing custom SQL file import for all {args.DDLFromFile}")
        tdc = transactionDataClient()
        for sql in args.DDLFromFile:
            tdc.generateFromSqlFile(sql, "sql")
        tdc.closeConnection()

    if args.debugDDL:
        print(f"performing DDL for article table, DEBUGGING {args.debugDDL}")

        tdc = transactionDataClient()

        newArticle = Article(
            "examplewebsite.com",
            "This is the header",
            "This is the originalText",
            "this would be the chatGPT response in paragraph form",
            10.23,
            22.40,
            0,
        )
        tdc.insert(newArticle)
        newPolitician = Politician(
            "Donald",
            "Trump",
            "John did some incredible things",
            32,
            "Male",
            0,
            "\img\imghere",
            "another more general summary here",
            "This would be a politcian byline",
            "this would be their politicial Position",
            "LNP",
            "AUS",
        )

        # update the attributes on this, remember to update the attributes on the API also.
        tdc.insert(newPolitician)
        newPolling = Polling(1, "Your mom?", "opt1", "op12", "op3", "op4", 0)
        tdc.insert(newPolling)

        # Article_ArticleBias Table
        newArticle_ArticleBias = Article_ArticleBias(
            newArticle.getId(),
            "Devastating blaze",
            'the term "devastating" indicates a tragice loss of life',
            0,
        )
        tdc.insert(newArticle_ArticleBias)
        biasSubtext = {
            "Devastating blaze": 'the term "devastating" indicates a tragice loss of life',
            "Terror Attack": 'The term "terror" is frightening and is used to emote panic',
        }
        newPoliticianCampaignPolicies = Politician_CampaignPolicies(
            "Donald",
            "Trump",
            "Affordable Housing",
            "I want to make housing affordable",
            0,
        )  # have to edit this in
        tdc.insert(newPoliticianCampaignPolicies)
        newComment = Comments(
            "examplewebsite.com", "Donald Trump", "this would be a comment", 0
        )

        print(newPolitician)
        print(newArticle)
        print(newArticle_ArticleBias)
        print(newPoliticianCampaignPolicies)
        print(newComment)

        tdc.closeConnection()

    if args.query is not None:
        print(f"performing sql query on table/s {args.query}")
        tdc = transactionDataClient()
        for i in args.query:
            print(tdc.query(i))
        tdc.closeConnection()

    if args.customImport is not None:
        print(
            f"performing custom SQL query for file/s {args.customImport} under /query:"
        )
        tdc = transactionDataClient()
        for sql in args.customImport:
            print(tdc.generateFromSqlFile(sql, "query"))
        tdc.closeConnection()

    if args.buildDB:
        print(f"performing custom SQL file import for all files under /inf/sql:")
        directory = "inf/sql"
        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
        print(files)
        tdc = transactionDataClient()
        for file in files:
            tdc.generateFromSqlFile(file, "sql")
        tdc.closeConnection()

    if args.DELETEALL:
        print('deleting all records')
        text = input("are you sure you want to delete all records (y/n)")
        
        tables = [
            'Politician_KeyTable',
            'Politician',
            'Polling',
            'Comments',
            'Politician_CampaignPoliciesByID',
            'Article',
            'Article_ArticleBias',
            'Politician_CampaignPolicies']
        if text == 'y': 
            tdc = transactionDataClient()
            for tablename in tables:
                tdc.query_special(F"DELETE FROM {tablename} WHERE 1=1")
                tdc.logMessage(messageStatus.SUCCESS, f"Successfully removed table {tablename}")
            print("COMPLETED")
        