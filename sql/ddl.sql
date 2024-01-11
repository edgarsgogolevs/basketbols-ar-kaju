create table games
(
    id         int identity
        constraint games_pk
            primary key,
    team_home  int  not null,
    team_away  int  not null,
    home_won   bit,
    updated_at datetime default getdate(),
    score_home int,
    score_away int,
    game_date  date not null,
    MIN        int,
    FGM        int,
    FGA        int,
    FG_PCT     float,
    FG3M       int,
    FG3A       int,
    FG3_PCT    float,
    FTM        int,
    FTA        int,
    FT_PCT     float,
    OREB       int,
    DREB       int,
    REB        int,
    AST        int,
    STL        int,
    BLK        int,
    TOV        int,
    PF         int
)
go

create unique index games_unique_idx
    on games (team_home, team_away, game_date)
go

CREATE TRIGGER games_updated_at
        ON basketball.games
        AFTER UPDATE
                AS
        BEGIN
        UPDATE basketball.games
        SET updated_at = GETDATE()
        WHERE id IN (SELECT id FROM inserted);
END;
go

create table prediction_models
(
    id                int identity
        constraint prediction_models_pk
            primary key,
    name              nvarchar(1000) not null collate SQL_Latin1_General_CP1_CI_AS,
    description       nvarchar(1000) collate SQL_Latin1_General_CP1_CI_AS,
    path              nvarchar(1000) not null collate SQL_Latin1_General_CP1_CI_AS,
    profile_picture   nvarchar(1000) not null collate SQL_Latin1_General_CP1_CI_AS,
    updated_at        datetime default getdate(),
    nominal_precision float,
    picture_small     nvarchar(1000) collate SQL_Latin1_General_CP1_CI_AS
)
go

create table game_predictions
(
    game_id            int   not null
        constraint game_predictions_games_id_fk
            references games,
    model_id           int   not null
        constraint game_predictions_prediction_models_id_fk
            references prediction_models,
    home_wins          bit   not null,
    prediction_correct bit,
    updated_at         datetime default getdate(),
    home_winning_proba float not null,
    constraint game_predictions_pk
        primary key (model_id, game_id)
)
go

CREATE TRIGGER game_predictions_updated_at
    ON basketball.game_predictions
    AFTER UPDATE
    AS
BEGIN
    UPDATE basketball.game_predictions
    SET updated_at = GETDATE()
    WHERE game_id = (SELECT game_id FROM inserted) and model_id = (SELECT game_predictions.model_id FROM inserted);
END;
go

CREATE TRIGGER prediction_models_updated_at
    ON basketball.prediction_models
    AFTER UPDATE
    AS
BEGIN
    UPDATE basketball.prediction_models
    SET updated_at = GETDATE()
    WHERE id IN (SELECT id FROM inserted);
END;
go

create table teams
(
    name        nvarchar(200) not null collate SQL_Latin1_General_CP1_CI_AS,
    logo_url    nvarchar(1000) collate SQL_Latin1_General_CP1_CI_AS,
    nba_url     nvarchar(1000) collate SQL_Latin1_General_CP1_CI_AS,
    town        nvarchar(500) collate SQL_Latin1_General_CP1_CI_AS,
    description text collate SQL_Latin1_General_CP1_CI_AS,
    abbr        nvarchar(3)   not null collate SQL_Latin1_General_CP1_CI_AS
        constraint teams_abbr_unique
            unique,
    id          int identity,
    updated_at  datetime default getdate(),
    conference  nvarchar(50) collate SQL_Latin1_General_CP1_CI_AS
)
go

CREATE TRIGGER updated_at_teams
    ON basketball.teams
    AFTER UPDATE
    AS
    BEGIN
    UPDATE basketball.teams
    SET updated_at = GETDATE()
    WHERE id IN (SELECT id FROM inserted);
END;
go

grant delete, insert, select, update on teams to api
go

