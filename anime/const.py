class Const:
    
    query_by_title = '''
        query {
            searchWorks(
                titles: ["%s"],
                orderBy: { field: WATCHERS_COUNT, direction: DESC }
            ) {
                edges {
                    node {
                        title
                        officialSiteUrl 
                        image {
                            recommendedImageUrl
                        }
                        casts {
                            edges {
                                node {
                                    character {
                                        name
                                    }
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
    '''