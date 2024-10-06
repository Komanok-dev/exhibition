from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


class DatabaseSettings(Settings):
    model_config = SettingsConfigDict(env_prefix='DATABASE_')
    DRIVER: str
    SYNCDRIVER: str
    USERNAME: str
    PASSWORD: str
    HOSTNAME: str
    PORT: str
    NAME: str
    TESTNAME: str

    @property
    def url(self) -> str:
        driver, user, password, host, port, name = (
            self.DRIVER,
            self.USERNAME,
            self.PASSWORD,
            self.HOSTNAME,
            self.PORT,
            self.NAME,
        )
        return f'{driver}://{user}:{password}@{host}:{port}/{name}'

    @property
    def test_url(self) -> str:
        driver, user, password, host, port, testname = (
            self.DRIVER,
            self.USERNAME,
            self.PASSWORD,
            self.HOSTNAME,
            self.PORT,
            self.TESTNAME,
        )
        return f'{driver}://{user}:{password}@{host}:{port}/{testname}'

    @property
    def test_sync_url(self) -> str:
        syncdriver, user, password, host, port, testname = (
            self.SYNCDRIVER,
            self.USERNAME,
            self.PASSWORD,
            self.HOSTNAME,
            self.PORT,
            self.TESTNAME,
        )
        return f'{syncdriver}://{user}:{password}@{host}:{port}/{testname}'


database_settings = DatabaseSettings()
