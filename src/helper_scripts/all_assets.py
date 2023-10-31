def all_assets_query(current_page: int, per_page: int) -> dict:
    query = """
    query ($current_page: PosInteger!, $per_page: PosInteger!) {
        allAssets {
            totalCount
            data(currentPage: $current_page, perPage: $per_page) {
                currentPage
                totalPages
                assets {
                    ... on Inverter {
                        remoteId
                        name
                        operationalConstraints {
                            efficiency
                            ratedPower
                        }
                        adapterConfiguration {
                            name
                            simulation {
                                enabled
                            }
                        }
                        connectedBatteries {
                            remoteId
                            operationalConstraints {
                                ratedPower
                                ratedEnergy
                            }
                            controlConstraints {
                                minimumStateOfCharge
                                maximumStateOfCharge
                            }
                        }
                        connectedPhotovoltaics {
                            remoteId
                            operationalConstraints {
                                ratedPower
                            }
                        }
                    }
                }
            }
        }
    }
    """

    variables = {"current_page": current_page, "per_page": per_page}

    return {"query": query, "variables": variables}
