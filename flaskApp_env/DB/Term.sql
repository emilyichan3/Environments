/****** Object:  Table [dbo].[Membership]    Script Date: 11/29/2021 2:35:42 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Term](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[Term] [nvarchar](6) NOT NULL,
	[Description] [nvarchar](200) NOT NULL,
	[Member_Pre] [nvarchar](6) NOT NULL,
	[Member_NextSeq] [int] NOT NULL,
	[ValidDateFm] [datetime] NOT NULL,
	[ValidDateTo] [datetime] NOT NULL,
	[Name] [nvarchar](50) NOT NULL
 CONSTRAINT [PK_Term] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

