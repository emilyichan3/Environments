USE [TIALTD]
GO

/****** Object:  Table [dbo].[Member]    Script Date: 11/29/2021 1:48:56 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Member](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Member_ID] [varchar](20) NOT NULL,
	[Period] [varchar](6) NOT NULL,
	[Activate] [int] NOT NULL,
	[Name] [varchar](60) NOT NULL,
	[MainMemberId] [varchar](20) NOT NULL,
	[MembershipType] [int] NOT NULL,
	[Email1] [varchar](120) NOT NULL,
	[Email2] [varchar](120) NOT NULL,
	[Email3] [varchar](120) NOT NULL,
	[Email4] [varchar](120) NOT NULL,
	[Phone1] [varchar](120) NOT NULL,
	[Phone2] [varchar](120) NOT NULL,
	[Phone3] [varchar](120) NOT NULL,
	[Phone4] [varchar](120) NOT NULL,
	[ValidDateFm] [datetime] NOT NULL,
	[ValidDateTo] [datetime] NOT NULL,
	[ValidCheckDate] [datetime] NOT NULL,
	[ValidDays] [int] NOT NULL,
	[SendEmailDate] [datetime] NOT NULL,
	[MembershipChangedPeriod] [varchar](6) NOT NULL,
	[Image_file] [varchar](50) NOT NULL,
	[Password] [varchar](60) NOT NULL,
	[NationalCode] [varchar](50) NOT NULL,
	[StopContact] [int] NOT NULL,
	[Comment] [varchar](200) NOT NULL,
 CONSTRAINT [PK_Member_1] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

