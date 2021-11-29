USE [TIALTD]
GO

/****** Object:  Table [dbo].[Membership]    Script Date: 11/29/2021 2:35:42 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Option](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Company] [nvarchar](50) NOT NULL,
	[Description] [nvarchar](200) NOT NULL,
	[CurrentTerm] [nvarchar](6) NOT NULL
 CONSTRAINT [PK_Option] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

