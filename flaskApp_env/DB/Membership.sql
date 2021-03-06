USE [TIALTD]
GO

/****** Object:  Table [dbo].[Membership]    Script Date: 11/29/2021 2:35:42 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Membership](
	[ID] [int] NOT NULL,
	[MembershipCode] [nvarchar](20) NULL,
	[MembershipName] [nvarchar](50) NULL,
 CONSTRAINT [PK_Membership] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

