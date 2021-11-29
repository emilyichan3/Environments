USE [TIALTD]
GO

/****** Object:  Table [dbo].[Post]    Script Date: 11/29/2021 2:35:58 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Post](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[title] [varchar](100) NOT NULL,
	[date_posted] [datetime] NOT NULL,
	[post_content] [varchar](1000) NOT NULL,
	[member_id] [int] NULL,
 CONSTRAINT [PK_Post_1] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Post]  WITH CHECK ADD FOREIGN KEY([member_id])
REFERENCES [dbo].[Member] ([id])
GO

