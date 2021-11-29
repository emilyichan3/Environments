USE [TIALTD]
GO

/****** Object:  Table [dbo].[Country]    Script Date: 11/29/2021 2:34:40 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Country](
	[CountryCode] [varchar](3) NOT NULL,
	[CountryName] [nvarchar](250) NOT NULL,
	[CountryNameEN] [varchar](20) NULL,
 CONSTRAINT [PK_Province] PRIMARY KEY CLUSTERED 
(
	[CountryCode] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

